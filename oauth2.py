import requests


class OAuth2:
    def __init__(self, client_id, client_secret):
        self.token_url = "https://osu.ppy.sh/oauth/token"

        self.client_id = client_id
        self.client_secret = client_secret

    def get_access_token(self):
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials",
            "scope": "public",
        }

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        r = requests.post(self.token_url, data=data, headers=headers)
        if r.status_code != 200:
            print(f"[ERROR] [{r.status_code}]")
            exit(1)

        response = r.json()
        return response
