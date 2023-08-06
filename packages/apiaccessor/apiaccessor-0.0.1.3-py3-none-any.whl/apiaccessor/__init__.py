import json
from time import time
import requests
name = 'apiaccessor'


class OAuth2:
    # The OAuth2 class handles OAuth2 Authentication
    def __init__(self, token_url, refresh_url, validate_url, client_id, client_secret):
        self.token_url = token_url
        self.refresh_url = refresh_url
        self.validate_url = validate_url
        # client credentials
        # client_id and client_secret should be hardcoded
        self.client_id = client_id
        self.client_secret = client_secret
        # token data
        self.access_token = ''
        self.expires_at = 0
        self.refresh_token = ''

    def get_token(self, username, password):
        # This requests and receives a token from the server
        # returns access token
        # username and password should be user input
        payload = {'client_id': self.client_id,
                   'client_secret': self.client_secret,
                   'username': username,
                   'password': password,
                   'grant_type': 'password'}
        try:
            t = json.loads(requests.post(self.token_url, data=payload).text)
        # If a token is not issued, catch the error
        except json.decoder.JSONDecodeError:
            print(requests.post(self.refresh_url, data=payload).text)
        # write token to memory
        print('token received')
        self.access_token = t['access_token']
        self.expires_at = t['expires_in'] + time()
        self.refresh_token = t['refresh_token']
        # return token
        return t['access_token']

    def refresh_token(self):
        # This will refresh the token if the token has expired
        # returns nothing, write the token to memory
        print('refresh token')
        # refresh token after it expires
        payload = {'client_id': self.client_id,
                   'client_secret': self.client_secret,
                   'refresh_token': self.refresh_token,
                   'grant_type': 'refresh_token'}
        try:
            t = json.loads(requests.post(self.refresh_url, data=payload).text)
        except json.decoder.JSONDecodeError:
            print(requests.post(self.refresh_url, data=payload).text)
        else:
            self.expires_at = t['expires_in'] + time()
            self.access_token = t['access_token']

    def validate_token(self):
        # This will check if the token is valid or not
        # returns a boolean based on the validity of the token
        t = json.loads(requests.post(self.validate_url, data={'token': self.access_token}).text)
        if 'error' in t:
            return False
        else:
            return True


class XAPIKey:
    def __init__(self, url, key_name, key):
        self.data = []
        self.url = url
        self.headers = {key_name: key}
        self.timeout = 1

    # Reads from data from API
    def reader(self, path, query):
        r = requests.get(self.url + path, headers=self.headers, params=query).text
        return r

