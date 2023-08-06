import pytest

from mocket.plugins.httpretty import HTTPretty
from mocket import Mocketizer


@pytest.mark.asyncio
async def test_simpl_all(async_games_client, register_json):
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

        users = await async_games_client.users.all()
        assert len(users) == 3


@pytest.mark.asyncio
async def test_game_save(async_games_client, register_json):
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

        game = await async_games_client.games.get(slug='simpl-demo')

        saved = await game.save()
        assert saved.slug == 'simpl-demo'


@pytest.mark.asyncio
async def test_simpl_filter(async_games_client, register_json):
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

        users = await async_games_client.users.filter(role="player")
        assert len(users) == 2


@pytest.mark.asyncio
async def test_simpl_get_id(async_games_client, register_json):
    with Mocketizer():
        register_json(HTTPretty.GET, '/users/2/', json={
            'id': 2,
            'username': 'user2',
            'role': 'player',
        })

        user2 = await async_games_client.users.get(id=2)
        assert user2.username == 'user2'

    with Mocketizer():
        register_json(HTTPretty.GET, '/users/9999/', status=404)

        with pytest.raises(async_games_client.ResourceNotFound):
            await async_games_client.users.get(id=9999)


@pytest.mark.asyncio
async def test_simpl_get_params(async_games_client, register_json):
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

        with pytest.raises(async_games_client.MultipleResourcesFound):
            await async_games_client.users.get(role='player')

    with Mocketizer():
        register_json(HTTPretty.GET, '/users/?role=cookie_monster', json=[])

        with pytest.raises(async_games_client.ResourceNotFound):
            await async_games_client.users.get(role='cookie_monster')

    with Mocketizer():
        register_json(HTTPretty.GET, '/users/?role=facilitator', json=[
            {
                'id': 3,
                'username': 'user3',
                'role': 'facilitator',
            },
        ])

        facilitator = await async_games_client.users.get(role='facilitator')
        assert facilitator.username == 'user3'


@pytest.mark.asyncio
async def test_simpl_bulk_unauthd(async_games_client, register_json):
    with Mocketizer():
        register_json(HTTPretty.GET, '/bulk/users/', status=403)

        with pytest.raises(async_games_client.NotAuthenticatedError):
            resources = await async_games_client.bulk.users.all()
            assert resources is None


@pytest.mark.asyncio
async def test_simpl_bulk_create(async_games_client, register_json):
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

        resources = await async_games_client.bulk.users.create(payload)
        assert resources is None

    with Mocketizer():
        register_json(HTTPretty.POST, '/bulk/users/', json=payload, status=201)

        resources = await async_games_client.bulk.users.create(payload, return_ids=True)
        assert len(resources) == 2
        assert resources[0] == 1

    with Mocketizer():
        register_json(HTTPretty.POST, '/bulk/users/', json=payload, status=500)

        with pytest.raises(async_games_client.HTTPError):
            await async_games_client.bulk.users.create(payload)

@pytest.mark.asyncio
async def test_simpl_bulk_delete(async_games_client, register_json):
    with Mocketizer():
        register_json(HTTPretty.DELETE, '/bulk/users/?id__in=1&id__in=2', status=204)

        resources = await async_games_client.bulk.users.delete(id__in=[1, 2])
        assert resources is None

    with Mocketizer():
        register_json(HTTPretty.DELETE, '/bulk/users/?id__in=1&id__in=2', status=500)

        with pytest.raises(async_games_client.HTTPError):
            await async_games_client.bulk.users.delete(id__in=[1, 2])
