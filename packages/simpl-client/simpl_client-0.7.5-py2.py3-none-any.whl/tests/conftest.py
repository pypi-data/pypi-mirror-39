import json as jsonlib

import pytest

from mocket.plugins.httpretty import HTTPretty

from simpl_client.async import GamesAPIClient as AsyncGamesAPIClient
from simpl_client.sync import GamesAPIClient as SyncGamesAPIClient

SIMPL_GAMES_URL = 'http://dummy.org'
SIMPL_GAMES_AUTH = ('user', 'user')


@pytest.fixture
def simpl_url():
    return SIMPL_GAMES_URL


@pytest.fixture
def simpl_auth():
    return SIMPL_GAMES_AUTH


@pytest.fixture
def async_games_client(simpl_url, simpl_auth):
    return AsyncGamesAPIClient(url=simpl_url, auth=simpl_auth)


@pytest.fixture
def sync_games_client(simpl_url, simpl_auth):
    return SyncGamesAPIClient(url=simpl_url, auth=simpl_auth)


@pytest.fixture
def register_json(simpl_url):
    def fn(method, url, json=None, **kwargs):
        if json is not None:
            body = jsonlib.dumps(json)
        else:
            body = ''
        kwargs.setdefault('content-type', 'application/json')
        kwargs.setdefault('match_querystring', True)
        return HTTPretty.register_uri(method, simpl_url + url, body, **kwargs)

    return fn
