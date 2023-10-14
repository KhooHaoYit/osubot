import requests


class osuAPI:
    def __init__(self, token):
        self.token = token
        self.api_url = "https://osu.ppy.sh/api/v2"

    def _get_request(self, endpoint):
        headers = {
            "Authorization": f"Bearer {self.token}",
        }
        url = self.api_url + endpoint

        r = requests.get(url, headers=headers)
        return r.json()

    def get_ranking(self, mode="osu", country="MY", page=1):
        endpoint = f"/rankings/{mode}/performance?country={country}&page={page}"
        res = self._get_request(endpoint)
        return res

    def get_user(self, user_id, mode="osu"):
        endpoint = f"/users/{user_id}?mode={mode}"
        res = self._get_request(endpoint)
        return res

    def get_user_best(self, user_id, mode="osu", offset=0, limit=100):
        endpoint = (
            f"/users/{user_id}/scores/best?mode={mode}&offset={offset}&limit={limit}"
        )
        res = self._get_request(endpoint)
        return res
