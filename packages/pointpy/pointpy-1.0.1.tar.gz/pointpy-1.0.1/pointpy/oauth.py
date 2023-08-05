import requests
import time


class PointOAuthError(Exception):
    pass


class PointCredentialsManager(object):
    OAUTH_TOKEN_URL = 'https://api.minut.com/v1/oauth/token'

    def __init__(self, client_id, client_secret, username, password):
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password

        self.token_info = None

    def _request_access_token(self):
        response = requests.post(self.OAUTH_TOKEN_URL, data={
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'username': self.username,
            'password': self.password,
            'grant_type': 'password',
        })

        if response.status_code != 200:
            raise PointOAuthError(response.reason)

        return response.json()

    def is_token_expired(self, token_info):
        now = int(time.time())

        return token_info['expires_at'] - now < 60

    def get_access_token(self):
        if self.token_info and not self.is_token_expired(self.token_info):
            return self.token_info['access_token']

        token_info = self._request_access_token()
        token_info = self._add_custom_values_to_token_info(token_info)
        self.token_info = token_info

        return self.token_info['access_token']

    def _add_custom_values_to_token_info(self, token_info):
        token_info['expires_at'] = (
            int(time.time()) + int(token_info['expires_in'])
        )

        return token_info
