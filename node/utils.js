import { readFile, writeFile } from 'fs/promises';
import { dirname } from 'path';
import { fileURLToPath } from 'url';
import { env } from './env';
import { spawn } from 'child_process';

const __dirname = dirname(fileURLToPath(import.meta.url));

export async function runPython(mode) {
  const child = spawn('python3', ['main.py', '--mode', mode], { stdio: 'inherit' });
  await new Promise(rs => child.once('exit', rs));
}

export async function getData(mode) {
  return await readFile(`${__dirname}/../data/${mode}.json`)
    .then(buf => JSON.parse(buf))
    .catch(() => null)
}

export async function prepareConfig() {
  await writeFile(`${__dirname}/../config.py`, `
client_id = ${JSON.stringify(env.OSU_CLIENT_ID)}
client_secret = ${JSON.stringify(env.OSU_CLIENT_SECRET)}
top_N = ${env.TOP_AMOUNT}
country = ${JSON.stringify(env.TARGET_COUNTRY)}

discord_token = ${JSON.stringify(env.DISCORD_TOKEN)}

osu_mode = {
  "osu": {
    "icon": "https://i.ppy.sh/abd6cb4889b2d418fb303a5137090bf2aea922b9/68747470733a2f2f6f73752e7070792e73682f68656c702f77696b692f536b696e6e696e672f496e746572666163652f696d672f6d6f64652d6f73752d6d65642e706e67",
    "color": 0xFF2D00,
    "text": "osu!standard",
    "discord_channel": [${env.CHANNEL_IDS_OSU.join(', ')}],
  },
  "taiko": {
    "icon": "https://i.ppy.sh/5524006ee3d7c598c6b6462b84f9a2f8fbc1516e/68747470733a2f2f6f73752e7070792e73682f68656c702f77696b692f536b696e6e696e672f496e746572666163652f696d672f6d6f64652d7461696b6f2d6d65642e706e67",
    "color": 0x46FF00,
    "text": "osu!taiko",
    "discord_channel": [${env.CHANNEL_IDS_TAIKO.join(', ')}],
  },
  "fruits": {
    "icon": "https://i.ppy.sh/2c30813a0dc967ff0cc960d6e6cc79620f221f41/68747470733a2f2f6f73752e7070792e73682f68656c702f77696b692f536b696e6e696e672f496e746572666163652f696d672f6d6f64652d6672756974732d6d65642e706e67",
    "color": 0x00FFEC,
    "text": "osu!catch",
    "discord_channel": [${env.CHANNEL_IDS_CATCH.join(', ')}],
  },
  "mania": {
    "icon": "https://i.ppy.sh/000bf1b2a22600864fd0ee9900acc21420397781/68747470733a2f2f6f73752e7070792e73682f68656c702f77696b692f536b696e6e696e672f496e746572666163652f696d672f6d6f64652d6d616e69612d6d65642e706e67",
    "color": 0xD500FF,
    "text": "osu!mania",
    "discord_channel": [${env.CHANNEL_IDS_MANIA.join(', ')}],
  },
}
`);
}
