from datetime import datetime
from datetime import tzinfo
from datetime import timedelta

import discord
import asyncio


class UTC8(tzinfo):
    def utcoffset(self, dt):
        return timedelta(hours=8)

    def dst(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return "UTC+8"


def str2dt(dt):
    dt = datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S%z")
    return dt


def dt2str(dt: datetime):
    dt = dt.strftime("%Y-%m-%dT%H:%M:%S%z")
    return dt


def get_current_time():
    now = datetime.now(tz=UTC8())
    return now


class discordAPI:
    def __init__(self, token):
        self.token = token
        self.client = discord.Client()

    def send_message(self, msg, channels):
        @self.client.event
        async def on_ready():
            print("Logged in as")
            print(self.client.user.name)
            print(self.client.user.id)
            print("------")

            for _channel in channels:
                channel = self.client.get_channel(_channel)
                for m in msg:
                    if m["embed"]:
                        await channel.send(embed=m["msg"])
                    else:
                        await channel.send(m["msg"])
                    await asyncio.sleep(1)
            await self.client.close()

        self.client.run(self.token, bot=True)
