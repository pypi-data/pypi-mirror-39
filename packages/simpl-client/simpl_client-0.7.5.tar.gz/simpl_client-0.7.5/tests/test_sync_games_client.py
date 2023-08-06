import pytest

from mocket.plugins.httpretty import HTTPretty
from mocket import Mocketizer


def test_simpl_all(sync_games_client, register_json):
    with Mocketizer():
        register_json(HTTPretty.GET, '/users/', json=[
            {
                'id': 1,
                'username': 'user1',
                'role': 'player',
            },
            {
                'id': 2,
                'username': 'user2',
                'role': 'player',
            },
            {
                'id': 3,
                'username': 'user3',
                'role': 'facilitator',
            },
        ])

        users = sync_games_client.users.all()
        assert len(users) == 3


def test_game_save(sync_games_client, register_json):
    with Mocketizer():
        register_json(HTTPretty.PUT, '/games/simpl-demo/', json={
            'id': 1,
            'slug': 'simpl-demo',
        })

        register_json(HTTPretty.GET, '/games/simpl-demo/', json={
            'id': 1,
            'slug': 'simpl-demo',
        })

        register_json(HTTPretty.PUT, '/games/1/', status=404)

        game = sync_games_client.games.get(slug='simpl-demo')

        saved = game.save()
        assert saved.slug == 'simpl-demo'


def test_simpl_filter(sync_games_client, register_json):
    with Mocketizer():
        register_json(HTTPretty.GET, '/users/?role=player', json=[
            {
                'id': 1,
                'username': 'user1',
                'role': 'player',
            },
            {
                'id': 2,
                'username': 'user2',
                'role': 'player',
            },
        ])

        users = sync_games_client.users.filter(role="player")
        assert len(users) == 2



def test_simpl_get_id(sync_games_client, register_json):
    with Mocketizer():
        register_json(HTTPretty.GET, '/users/2/', json={
            'id': 2,
            'username': 'user2',
            'role': 'player',
        })

        user2 = sync_games_client.users.get(id=2)
        assert user2.username == 'user2'

    with Mocketizer():
        register_json(HTTPretty.GET, '/users/9999/', status=404)

        with pytest.raises(sync_games_client.ResourceNotFound):
            sync_games_client.users.get(id=9999)



def test_simpl_get_params(sync_games_client, register_json):
    with Mocketizer():
        register_json(HTTPretty.GET, '/users/?role=player', json=[
            {
                'id': 1,
                'username': 'user1',
                'role': 'player',
            },
            {
                'id': 2,
                'username': 'user2',
                'role': 'player',
            },
        ])

        with pytest.raises(sync_games_client.MultipleResourcesFound):
            sync_games_client.users.get(role='player')

    with Mocketizer():
        register_json(HTTPretty.GET, '/users/?role=cookie_monster', json=[])

        with pytest.raises(sync_games_client.ResourceNotFound):
            sync_games_client.users.get(role='cookie_monster')

    with Mocketizer():
        register_json(HTTPretty.GET, '/users/?role=facilitator', json=[
            {
                'id': 3,
                'username': 'user3',
                'role': 'facilitator',
            },
        ])

        facilitator = sync_games_client.users.get(role='facilitator')
        assert facilitator.username == 'user3'



def test_simpl_bulk_unauthd(sync_games_client, register_json):
    with Mocketizer():
        register_json(HTTPretty.GET, '/bulk/users/', status=403)

        with pytest.raises(sync_games_client.NotAuthenticatedError):
            resources = sync_games_client.bulk.users.all()
            assert resources is None



def test_simpl_bulk_create(sync_games_client, register_json):
    payload = [
        {
            'id': 1,
            'username': 'user1',
            'role': 'player',
        },
        {
            'id': 2,
            'username': 'user2',
            'role': 'player',
        },
    ]
    with Mocketizer():
        register_json(HTTPretty.POST, '/bulk/users/', json=payload, status=201)

        resources = sync_games_client.bulk.users.create(payload)
        assert resources is None

    with Mocketizer():
        register_json(HTTPretty.POST, '/bulk/users/', json=payload, status=201)

        resources = sync_games_client.bulk.users.create(payload,
                                                        return_ids=True)
        assert len(resources) == 2
        assert resources[0] == 1

    with Mocketizer():
        register_json(HTTPretty.POST, '/bulk/users/', json=payload, status=500)

        with pytest.raises(sync_games_client.HTTPError):
            sync_games_client.bulk.users.create(payload)



def test_simpl_bulk_delete(sync_games_client, register_json):
    with Mocketizer():
        register_json(HTTPretty.DELETE, '/bulk/users/?id__in=1&id__in=2',
                      status=204)

        resources = sync_games_client.bulk.users.delete(id__in=[1, 2])
        assert resources is None

    with Mocketizer():
        register_json(HTTPretty.DELETE, '/bulk/users/?id__in=1&id__in=2',
                      status=500)

        with pytest.raises(sync_games_client.HTTPError):
            sync_games_client.bulk.users.delete(id__in=[1, 2])
