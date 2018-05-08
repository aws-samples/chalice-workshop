Section 2: Add ``chalicelib`` to Todo application
=================================================

Users will learn about chalicelib in this section by moving the
in-memory db out of ``app.py`` and into ``chalicelib/db.py``

Our ``app.py`` file is getting a little bit crowded, and as our application
grows it's only going to get worse. To solve this problem we can create a
module called ``chalicelib`` that Chalice will deploy alongside the ``app.py``


.. contents::
   :local:
   :depth: 1



Create ``chalicelib`` module
----------------------------


Let's start this process by moving our database code out of ``app.py`` and into
``chalicelib``.

Instructions
~~~~~~~~~~~~

1. Create a new ``chalicelib`` directory alongside the ``app.py`` file::

     $ mkdir chalicelib


2. Since ``chalicelib`` is a Python module, it must have an ``__init__.py``
   file::

     $ touch chalicelib/__init__.py


3. Create a ``db.py`` file where all database interaction code will live::

     $ touch chalicelib/db.py


Verification
~~~~~~~~~~~~

The directory structure of your application should now look like this::

  $ tree .
  .
  ├── app.py
  ├── chalicelib
  │   ├── __init__.py
  │   └── db.py
  └── requirements.txt

  1 directory, 4 files


Move database code from ``app.py`` to the ``db.py``
---------------------------------------------------

Copy ``InMemoryTodoDB`` class from ``app.py`` to ``chalicelib/db.py``

Instructions
~~~~~~~~~~~~

1. Cut the class ``InMemoryTodoDB`` out of ``app.py`` and paste it into
   ``chalicelib/db.py`` using your favorite editor

2. Move the following lines from ``app.py`` to ``db.py``::

     from uuid import uuid4


     DEFAULT_USERNAME = 'default'


Verification
~~~~~~~~~~~~
Lets try running ``chalice local`` and check a few routes to see if they still
work::

  $ echo '{"description": "My first Todo", "metadata": {}}' | http POST localhost:8000/todos
  HTTP/1.1 500 Internal Server Error
  Content-Length: 459
  Content-Type: text/plain
  Date: Fri, 20 Oct 2017 20:58:37 GMT
  Server: BaseHTTP/0.3 Python/2.7.13

  Traceback (most recent call last):
    File "/Users/jcarlyl/.envs/workshop/lib/python2.7/site-packages/chalice/app.py", line 649, in _get_view_function_response
      response = view_function(**function_args)
    File "/private/tmp/chalice/add-db/app.py", line 24, in add_new_todo
      return get_app_db().add_item(
    File "/private/tmp/chalice/add-db/app.py", line 12, in get_app_db
      _DB = InMemoryTodoDB()
  NameError: global name 'InMemoryTodoDB' is not defined


Since ``InMemoryTodoDB`` has been moved it now needs to be imported.


Import ``InMemoryTodoDB`` from chalicelib
-----------------------------------------

Looks like we forgot to import the ``InMemoryTodoDB`` from ``chalicelib``.
Since ``InMemoryTodoDB`` is now in a different module, we need to import it.


Instructions
~~~~~~~~~~~~

1. At the top of ``app.py`` add the line::

     from chalicelib.db import InMemoryTodoDB


Verification
~~~~~~~~~~~~

Let's try that last step one more time::

  $ echo '{"description": "My first Todo", "metadata": {}}' | \
      http POST localhost:8000/todos
  HTTP/1.1 200 OK
  Content-Length: 36
  Content-Type: application/json
  Date: Fri, 20 Oct 2017 21:18:57 GMT
  Server: BaseHTTP/0.3 Python/2.7.13

  7fc955af-5a9e-42b5-ad3a-8f5017c91091


Now that it appears to work again let's finish verifying all the other routes
still work as expected, starting with checking the state::

  $ http localhost:8000/todos/7fc955af-5a9e-42b5-ad3a-8f5017c91091
  HTTP/1.1 200 OK
  Content-Length: 140
  Content-Type: application/json
  Date: Fri, 20 Oct 2017 21:21:03 GMT
  Server: BaseHTTP/0.3 Python/2.7.13

  {
      "description": "My first Todo",
      "metadata": {},
      "state": "unstarted",
      "uid": "7fc955af-5a9e-42b5-ad3a-8f5017c91091",
      "username": "default"
  }


Update the ``state`` of this Todo to ``started``::

  $ echo '{"state": "started"}' | \
      http PUT localhost:8000/todos/7fc955af-5a9e-42b5-ad3a-8f5017c91091
  HTTP/1.1 200 OK
  Content-Length: 4
  Content-Type: application/json
  Date: Fri, 20 Oct 2017 21:21:59 GMT
  Server: BaseHTTP/0.3 Python/2.7.13

  null


Check the ``state`` again to make sure that it is now ``started``::

  $ http localhost:8000/todos/7fc955af-5a9e-42b5-ad3a-8f5017c91091
  HTTP/1.1 200 OK
  Content-Length: 138
  Content-Type: application/json
  Date: Fri, 20 Oct 2017 21:23:16 GMT
  Server: BaseHTTP/0.3 Python/2.7.13

  {
      "description": "My first Todo",
      "metadata": {},
      "state": "started",
      "uid": "7fc955af-5a9e-42b5-ad3a-8f5017c91091",
      "username": "default"
  }


Final Code
----------

When you are finished your ``app.py`` file should look like:

.. literalinclude::  ../../../code/part1/03-add-dynamodb/app.py
  :linenos:
  :lines: 1-47

And your ``chalicelib/db.py`` file should look like:


.. code-block:: python

    from uuid import uuid4


    DEFAULT_USERNAME = 'default'


    class InMemoryTodoDB(object):
        def __init__(self, state=None):
            if state is None:
                state = {}
            self._state = state

        def list_all_items(self):
            all_items = []
            for username in self._state:
                all_items.extend(self.list_items(username))
            return all_items

        def list_items(self, username=DEFAULT_USERNAME):
            return self._state.get(username, {}).values()

        def add_item(self, description, metadata=None, username=DEFAULT_USERNAME):
            if username not in self._state:
                self._state[username] = {}
            uid = str(uuid4())
            self._state[username][uid] = {
                'uid': uid,
                'description': description,
                'state': 'unstarted',
                'metadata': metadata if metadata is not None else {},
                'username': username
            }
            return uid

        def get_item(self, uid, username=DEFAULT_USERNAME):
            return self._state[username][uid]

        def delete_item(self, uid, username=DEFAULT_USERNAME):
            del self._state[username][uid]

        def update_item(self, uid, description=None, state=None,
                        metadata=None, username=DEFAULT_USERNAME):
            item = self._state[username][uid]
            if description is not None:
                item['description'] = description
            if state is not None:
                item['state'] = state
            if metadata is not None:
                item['metadata'] = metadata
