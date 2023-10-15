import { getData, prepareConfig, runPython } from "./utils";

await prepareConfig();

`
osu
mania
fruits
taiko
`.trim().split('\n').map(mode => handleMode(mode));

async function handleMode(mode) {
  const nextRun = await getData(mode)
    .then(data => {
      if (!data)
        return 0;
      const savedTime = new Date(data.datetime);
      savedTime.setHours(0, 0, 0, 0);
      savedTime.setDate(savedTime.getDate() + 1);
      const remain = savedTime.getTime() - Date.now();
      return remain < 0 ? 0 : remain;
    });
  console.log(mode, 'next run:', new Date(Date.now() + nextRun) + '');
  setTimeout(async () => {
    await runPython(mode);
    handleMode(mode);
  }, nextRun);
}
