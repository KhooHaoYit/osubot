import os
import json
import argparse
from operator import itemgetter

import discord

from oauth2 import OAuth2
from osuAPI import osuAPI
import config
import utils


def get_data_dir():
    return "data/"


def get_old_score(mode):
    path = os.path.join(get_data_dir(), f"{mode}.json")
    if not os.path.exists(path):
        return {"users": [], "datetime": None}

    with open(path) as f:
        data = json.load(f)

    return data


def save_new_score(ranking, now, mode):
    for r in ranking:
        del r["user_best"]
        del r["avatar_url"]
        del r["country_rank"]

    data = {"users": ranking, "datetime": utils.dt2str(now)}

    if not os.path.exists(get_data_dir()):
        os.mkdir(get_data_dir())

    path = os.path.join(get_data_dir(), f"{mode}.json")
    with open(path, "w") as f:
        json.dump(data, f)


def create_osu_api_instance():
    oauth2 = OAuth2(config.client_id, config.client_secret)
    token = oauth2.get_access_token()
    api = osuAPI(token["access_token"])
    return api


def get_current_osu_ranking(mode):
    api = create_osu_api_instance()
    ranking = api.get_ranking(mode=mode, country=config.country)
    ranking = sorted(ranking["ranking"], key=itemgetter("pp"), reverse=True)

    current_ranking = []
    for i in range(config.top_N):
        user = ranking[i]
        user_best = api.get_user_best(user["user"]["id"])
        user_best = sorted(user_best, key=itemgetter("pp"), reverse=True)
        user_stats = {
            "pp": user["pp"],
            "username": user["user"]["username"],
            "id": user["user"]["id"],
            "global_rank": user["global_rank"],
            "avatar_url": user["user"]["avatar_url"],
            "country_rank": i + 1,
            "user_best": user_best,
        }

        current_ranking.append(user_stats)

    return current_ranking


def find_user_from_old_ranking(prev_ranking, user_id):
    for user in prev_ranking:
        if user["id"] == user_id:
            return user
    return None


def parse_ranking(prev_ranking, prev_dt, current_ranking):
    parsed_ranking = []

    for user in current_ranking:
        user_id = user["id"]
        old_user_stats = find_user_from_old_ranking(prev_ranking, user_id)

        if not old_user_stats or round(user["pp"]) != round(old_user_stats["pp"]):
            data = {
                "pp": user["pp"],
                "username": user["username"],
                "id": user["id"],
                "global_rank": user["global_rank"],
                "avatar_url": user["avatar_url"],
                "country_rank": user["country_rank"],
                "diff": "NEW"
                if not old_user_stats
                else round(user["pp"]) - round(old_user_stats["pp"]),
                "scores": [],
            }
            for score in user["user_best"]:
                score_date = utils.str2dt(score["created_at"])
                if score_date >= prev_dt:
                    new_score = {
                        "rank": score["rank"],
                        "pp": round(score["pp"]),
                        "artist": score["beatmapset"]["artist"],
                        "title": score["beatmapset"]["title"],
                        "version": score["beatmap"]["version"],
                        "mods": score["mods"],
                        "acc": score["accuracy"],
                        "url": score["beatmap"]["url"],
                    }
                    data["scores"].append(new_score)

            parsed_ranking.append(data)

    return parsed_ranking


def construct_discord_data(mode, ranking, prev_dt, now):
    embeds = []

    # date
    embed = {
        "author": {
            "name": f"{prev_dt.strftime('%d/%m')} -> {now.strftime('%d/%m')}",
            "icon_url": config.osu_mode[mode]["icon"],
        },
    }
    embeds.append(embed)

    # scores
    for r in ranking:
        diff = r["diff"]
        if diff != "NEW":
            diff = f"{r['diff']:+d}pp"

        embed = {
            "author": {
                "name": f"#{r['country_rank']} {r['username']} {round(r['pp']):,}pp ({diff})",
                "url": f"https://osu.ppy.sh/users/{r['id']}",
                "icon_url": r["avatar_url"],
            },
            "color": config.osu_mode[mode]["color"],
            "fields": [],
        }

        for s in r["scores"]:
            mods = " +" if s["mods"] else ""
            mods += ",".join(s["mods"]) + " "
            buf = f"{s['rank']} | {s['pp']}pp | "
            buf += f"[{s['artist']} - {s['title']} [{s['version']}]]({s['url']})"
            buf += f"{mods}({s['acc']:.2%})"

            embed_field = {
                "name": "||\n||",
                "value": buf.replace("*", "\\*"),  # escape italic
                "inline": False,
            }
            embed["fields"].append(embed_field)

        embeds.append(embed)

    # no scores
    if len(embeds) == 1:
        embed = {
            "author": {
                "name": "Where are the farmers?",
                "icon_url": config.osu_mode[mode]["icon"],
            },
        }
        embeds.append(embed)

    return embeds


def send_discord_message(embeds, mode):
    msg = []
    for e in embeds:
        msg.append({"embed": True, "msg": discord.Embed.from_dict(e)})

    discord_api = utils.discordAPI(config.discord_token)
    discord_api.send_message(msg, config.osu_mode[mode]["discord_channel"])


def main(mode):
    now = utils.get_current_time()

    old_score_json = get_old_score(mode)
    prev_ranking = old_score_json["users"]
    prev_datetime = None
    if not prev_ranking:
        prev_datetime = now
    else:
        prev_datetime = utils.str2dt(old_score_json["datetime"])

    current_ranking = get_current_osu_ranking(mode)
    parsed_ranking = parse_ranking(prev_ranking, prev_datetime, current_ranking)

    embeds = construct_discord_data(mode, parsed_ranking, prev_datetime, now)
    send_discord_message(embeds, mode)

    save_new_score(current_ranking, now, mode)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=["osu", "taiko", "fruits", "mania"],
        default="osu",
    )
    args = parser.parse_args()
    main(args.mode)
