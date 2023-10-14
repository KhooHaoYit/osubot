# osuBot

A osu! discord bot that get country top players ranking and show their recent scores

## Config

Create `config.py` with the following info:

```python
client_id = <your_osu_api_client_id>
client_secret = <your_osu_api_client_secret>
top_N = 30
country = "MY"

discord_token = <your_discord_bot_token>

osu_mode = {
    "osu": {
        "icon": "https://i.ppy.sh/abd6cb4889b2d418fb303a5137090bf2aea922b9/68747470733a2f2f6f73752e7070792e73682f68656c702f77696b692f536b696e6e696e672f496e746572666163652f696d672f6d6f64652d6f73752d6d65642e706e67",
        "color": 0xFF2D00,
        "text": "osu!standard",
        "discord_channel": [<your_discord_channel_id_1>, <id_2>],
    },
    "taiko": {
        "icon": "https://i.ppy.sh/5524006ee3d7c598c6b6462b84f9a2f8fbc1516e/68747470733a2f2f6f73752e7070792e73682f68656c702f77696b692f536b696e6e696e672f496e746572666163652f696d672f6d6f64652d7461696b6f2d6d65642e706e67",
        "color": 0x46FF00,
        "text": "osu!taiko",
        "discord_channel": [<your_discord_channel_id>],
    },
    "fruits": {
        "icon": "https://i.ppy.sh/2c30813a0dc967ff0cc960d6e6cc79620f221f41/68747470733a2f2f6f73752e7070792e73682f68656c702f77696b692f536b696e6e696e672f496e746572666163652f696d672f6d6f64652d6672756974732d6d65642e706e67",
        "color": 0x00FFEC,
        "text": "osu!catch",
        "discord_channel": [<your_discord_channel_id>],
    },
    "mania": {
        "icon": "https://i.ppy.sh/000bf1b2a22600864fd0ee9900acc21420397781/68747470733a2f2f6f73752e7070792e73682f68656c702f77696b692f536b696e6e696e672f496e746572666163652f696d672f6d6f64652d6d616e69612d6d65642e706e67",
        "color": 0xD500FF,
        "text": "osu!mania",
        "discord_channel": [<your_discord_channel_id>],
    },
}
```

## Run

```bash
pip3 install -r requirements.txt
python3 main.py --mode {osu,taiko,fruits,mania}
```