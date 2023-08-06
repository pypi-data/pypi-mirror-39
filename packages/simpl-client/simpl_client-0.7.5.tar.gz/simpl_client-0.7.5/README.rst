GamesAPIClient
==============

.. image:: https://travis-ci.com/simplworld/simpl-client.svg?token=cyqpBgqLC1o8qUptfcpE&branch=master
    :target: https://travis-ci.com/simplworld/simpl-client


Python clients for asynchronously accessing simpl-games-api.

Usage::

    from simpl_client.async import GamesAPIClient
    async_games_client = GamesAPIClient(url=SIMPL_GAMES_URL, auth=SIMPL_GAMES_AUTH)

to synchronously access simpl-games-api use::

    from simpl_client.sync import GamesAPIClient
    sync_games_client = GamesAPIClient(url=SIMPL_GAMES_URL, auth=SIMPL_GAMES_AUTH)

Installation
------------
::

    pip install simpl-client

Endpoints
---------

Endpoints are available as properties on the main instance.

``.all()``
~~~~~~~~~~

Retrieves all resources (essentially a simple ``GET`` on the endpoint)::

    async_games_client.runusers.all()  # GET /runusers/

``.filter(**kwargs)`` calls a ``GET`` with ``kwargs`` as querystring values::

    async_games_client.runusers.filter(run=12, world=1)  # GET /runusers/?run=12&world=1

``.get(**kwargs)``
~~~~~~~~~~~~~~~~~~

A special case of ``.filter()``.

If ``kwargs`` contains ``id``, ``pk``, ``slug`` or ``username``, that value will
be used in the URL path, in that order.

Otherwise, it calls a ``GET`` with ``kwargs`` as querystring values.

If the returned list is empty, will raise ``ResourceNotFound``.

If the returned list contains more than 1 resource, will raise ``MultipleResourcesFound``

Note that ``.get()`` will return a ``Resource``, not a list of ``Resource`` s

::

    async_games_client.runusers.filter(run=12, world=1)  # GET /runusers/?run=12&world=1
    async_games_client.runusers.filter(id=12)  # GET /runusers/12/
    async_games_client.users.filter(username='alice')  # GET /users/alice/

``.create(payload)``
~~~~~~~~~~~~~~~~~~~~

Will result in a ``POST``, with ``payload`` (a ``dict``) as the request's body,
returning a new ``Resource``::

    runuser = async_games_client.runusers.create({'run': 12, 'world': 1})  # POST /runusers/

``.get_or_create(defaults, **kwargs)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Issues a GET to fetch the resource. If the resource is not found, issues a POST
to create the resource.

    # Assuming it doesn't exist
    run = myclient.run.get_or_update(game=12, defaults={'active': True})  # GET /runs/?game=12, then POST /runs/


``.create_or_update(payload)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If ``payload`` contains a key called ``'id'``, will issue a ``PUT``, otherwise
it will call ``.create``::

    runuser = async_games_client.runusers.create_or_update({'id': 1234, 'world': 1})  # PUT /runusers/1234/


``.delete(pk)``
~~~~~~~~~~~~~~~

Will issue a ``DELETE``, and will use ``pk`` as part of the URL::

    async_games_client.runusers.delete(24)  # DELETE /runusers/24/

Resources
---------

All endpoints methods (with the exception of ``.delete()``) return either a
``Resource`` or a list of ``Resource`` s.

A ``Resource`` is just a wrapping class for a ``dict``, where keys can be accessed
as properties.

Additionally, ``Resource`` s have a special property called ``.payload``, which
contains the original payload received from the server.

``Resource`` s have the following methods:

``Resource.delete()`` will result in a ``DELETE``, with ``Resource.id`` as
par of the URL::

    runuser = async_games_client.runusers.create({'run': 12, 'world': 1})  # POST /runusers/
    runuser.delete()  # DELETE /runuser/345/ -- the ID 345 was returned by the server in the previous response

``Resource.save()`` will result in a ``PUT``, with ``Resource.id`` as
par of the URL::

    runuser = async_games_client.runusers.create({'run': 12, 'world': 1})  # POST /runusers/
    runuser.run = 13
    runuser.save()  # PUT /runuser/345/


Bulk requests
-------------

::

    async_games_client.bulk.results.create([...], return_ids=False)
    async_games_client.bulk.results.delete(**lookup)


Detail Routes
-------------

::

    async_games_client.scenario(id=123).rewind()


Setup development environment
-----------------------------
::

    git clone git@github.com:simplworld/simpl-client.git
    cd simpl-client
    mkvirtualenv simpl-client
    pip install -e .

Testing
-------
::

    python setup.py test

Running the tests requires having ``libmagic`` installed.

On OS X, simply run ``brew install libmagic``.

License
-------

Copyright © 2018 The Wharton School,  The University of Pennsylvania 

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
