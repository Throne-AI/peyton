import json
import random
import requests

from .competition import Competition
from .silly import random_play
from .user import User


class AuthError(Exception):
    pass


class ThrottleError(Exception):
    pass


class Throne(object):
    """
    Provides access to Throne.ai API
    
    import peyton
    throne = peyton.Throne(username='goat', token='your-token-here')

    """

    BASE_URL = 'https://www.throne.ai/api/'

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        pass

    def __init__(self, username, token):
        """
        Initializes and tests a connection
        """

        self.username = username
        self.token = token
        self.headers = {'Authorization': self.token, 'X-USERNAME': self.username}
        self._test_auth()

        self.competition = Competition(api=self)
        self.user = User(api=self)

    @staticmethod
    def _auth_report(result):
        """
        Raises authorization error if credentials are invalid
        """

        if result.status_code == 403:
            raise AuthError('Invalid credentials')     

        if result.status_code == 429:
            raise ThrottleError(json.loads(result.content.decode("utf-8"))['detail'])     

    def _test_auth(self):
        """
        Tests credentials upon initialization
        """
        result = requests.get('%s%s' % (self.BASE_URL, 'auth/'), headers=self.headers)
        self._auth_report(result)

    def omaha(self):
        """
        Make an audible
        """
        x = random.randint(0, 5)

        print(random_play(x))