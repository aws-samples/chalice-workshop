Section 1: Create initial Todo application
==========================================

For the rest of this workshop, we will be building a serverless Todo
application. The application will allow for creating Todo's, getting Todo's,
updating Todo's, and deleting Todo's. In terms of the REST API, it will
consist of the following:

============= =============== ============
HTTP Method   URI Path        Description
============= =============== ============
``GET``       ``/todos/``     Gets a list of all Todo's
``POST``      ``/todos/``     Creates a new Todo
``GET``       ``/todos/{id}`` Gets a specific Todo
``DELETE``    ``/todos/{id}`` Deletes a specific Todo
``PUT``       ``/todos/{id}`` Updates the state of a Todo
============= =============== ============

Furthermore, a Todo will have the following schema::

  {
    "description": {"type": "str"},
    "uid": {"type: "str"},
    "state": {"type: "str", "enum": ["unstarted", "started", "completed"]},
    "metadata": {
      "type": "object"
    },
    "username": {"type": "str"}
  }


This step will focus on how to build a simple in-memory version of the
Todo application. For this section we will be doing the following to create
this version of the application:

.. contents::
   :local:
   :depth: 1


Install Chalice
---------------

This step will ensure that ``chalice`` is installed in your virtualenv.

Instructions
~~~~~~~~~~~~

1. Install ``chalice`` inside of your virtualenv::

       $ pip install chalice


Verification
~~~~~~~~~~~~

To make sure ``chalice`` was installed correctly, run::

   $ chalice --version


Create a new Chalice project
----------------------------

Create the new Chalice project for the Todo application.

Instructions
~~~~~~~~~~~~

1. Create a new Chalice project called ``mytodo`` with the ``new-project``
   command::

       $ chalice new-project mytodo


Verification
~~~~~~~~~~~~

To ensure that the project was created, list the contents of the newly created
``mytodo`` directory::

    $ ls mytodo
    app.py           requirements.txt


It should contain an ``app.py`` file and a ``requirements.txt`` file.


Add the starting ``app.py``
---------------------------

Copy a boilerplate ``app.py`` file to begin working on the Todo application

Instructions
~~~~~~~~~~~~

1. If you have not already done so, clone the repository for this workshop::

      $ git clone https://github.com/aws-samples/chalice-workshop.git


2. Copy the over the ``app.py`` file to the ``mytodo`` Chalice application::

      $ cp ../chalice-workshop/code/part1/01-new-project/app.py mytodo/app.py


Verification
~~~~~~~~~~~~

To verify that the boilerplate application is working correctly, move into
the ``mytodo`` application directory and run ``chalice local`` to spin up
a version of the application running locally::

   $ cd mytodo
   $ chalice local
   Serving on localhost:8000


In a separate terminal window now install ``httpie``::

   $ pip install httpie


And make an HTTP request to application running the ``localhost``::

   $ http localhost:8000/todos
   HTTP/1.1 200 OK
   Content-Length: 2
   Content-Type: application/json
   Date: Thu, 19 Oct 2017 23:31:12 GMT
   Server: BaseHTTP/0.3 Python/2.7.10

   []

This should return an empty list back as there are no Todo's currently in
the application.


Add a route for creating a Todo
-------------------------------

Add a route for creating a Todo.

Instructions
~~~~~~~~~~~~

1. Open the ``app.py`` in an editor of your choice

2. At the bottom of the ``app.py`` file add a function called
   ``add_new_todo()``

3. Decorate the ``add_new_todo()`` function with a ``route`` that only
   accepts ``POST`` to the URI ``/todos``.

4. In the ``add_new_todo()`` function use the ``app.current_request.json_body``
   to add the Todo (which includes its description and metadata) to the
   database.

5. In the ``add_new_todo()`` function ``return`` the ID of the Todo that was
   added in the database.


.. The :emphasize-lines: option is relative to :lines:.

.. literalinclude:: ../../../code/part1/02-add-chalicelib/app.py
   :linenos:
   :lines: 69-75


Verification
~~~~~~~~~~~~

To verify that the new route works, run ``chalice local`` and in a separate
terminal window run the following using ``httpie``::

   $ echo '{"description": "My first Todo", "metadata": {}}' | http POST localhost:8000/todos
   HTTP/1.1 200 OK
   Content-Length: 36
   Content-Type: application/json
   Date: Thu, 19 Oct 2017 23:44:24 GMT
   Server: BaseHTTP/0.3 Python/2.7.10

   8cc673f0-7dd3-4e9d-a20b-245fcd34859d


This will return the ID of the Todo. For this example, it is ``8cc673f0-7dd3-4e9d-a20b-245fcd34859d``.
Now check that it is now listed when you retrieve all Todos::

    $ http localhost:8000/todos
    HTTP/1.1 200 OK
    Content-Length: 142
    Content-Type: application/json
    Date: Thu, 19 Oct 2017 23:46:53 GMT
    Server: BaseHTTP/0.3 Python/2.7.10

    [
        {
            "description": "My first Todo",
            "metadata": {},
            "state": "unstarted",
            "uid": "8cc673f0-7dd3-4e9d-a20b-245fcd34859d",
            "username": "default"
        }
    ]

Add a route for getting a specific Todo
---------------------------------------

Add a route for getting a specific Todo.


Instructions
~~~~~~~~~~~~

1. In the ``app.py``, add a function called ``get_todo()`` that accepts a
   ``uid`` as a parameter.

2. Decorate the ``get_todo()`` function with a ``route`` that only
   accepts ``GET`` to the URI ``/todos/{uid}``.

3. In the ``get_todo()`` function ``return`` the specific Todo item from the
   database using the ``uid`` function parameter.


  .. literalinclude:: ../../../code/part1/02-add-chalicelib/app.py
       :linenos:
       :lines: 78-80


Verification
~~~~~~~~~~~~

To verify that the new route works, run ``chalice local`` and in a separate
terminal window run the following using ``httpie``::

   $ echo '{"description": "My first Todo", "metadata": {}}' | http POST localhost:8000/todos
   HTTP/1.1 200 OK
   Content-Length: 36
   Content-Type: application/json
   Date: Thu, 19 Oct 2017 23:44:24 GMT
   Server: BaseHTTP/0.3 Python/2.7.10

   8cc673f0-7dd3-4e9d-a20b-245fcd34859d


Now use the returned ID ``8cc673f0-7dd3-4e9d-a20b-245fcd34859d`` to request
the specific Todo::

    $ http localhost:8000/todos/8cc673f0-7dd3-4e9d-a20b-245fcd34859d
    HTTP/1.1 200 OK
    Content-Length: 140
    Content-Type: application/json
    Date: Thu, 19 Oct 2017 23:52:35 GMT
    Server: BaseHTTP/0.3 Python/2.7.10

    {
        "description": "My first Todo",
        "metadata": {},
        "state": "unstarted",
        "uid": "8cc673f0-7dd3-4e9d-a20b-245fcd34859d",
        "username": "default"
    }


Add a route for deleting a specific Todo
----------------------------------------

Add a route for deleting a specific Todo.

Instructions
~~~~~~~~~~~~

1. In the ``app.py``, add a function called ``delete_todo()`` that accepts a
   ``uid`` as a parameter.

2. Decorate the ``delete_todo()`` function with a ``route`` that only
   accepts ``DELETE`` to the URI ``/todos/{uid}``.

3. In the ``delete_todo()`` function delete the Todo from the database using
   the ``uid`` function parameter.

.. literalinclude:: ../../../code/part1/02-add-chalicelib/app.py
   :linenos:
   :lines: 83-85


Verification
~~~~~~~~~~~~

To verify that the new route works, run ``chalice local`` and in a separate
terminal window run the following using ``httpie``::

   $ echo '{"description": "My first Todo", "metadata": {}}' | http POST localhost:8000/todos
   HTTP/1.1 200 OK
   Content-Length: 36
   Content-Type: application/json
   Date: Thu, 19 Oct 2017 23:44:24 GMT
   Server: BaseHTTP/0.3 Python/2.7.10

   8cc673f0-7dd3-4e9d-a20b-245fcd34859d

Now check that it is now listed when you retrieve all Todos::

    $ http localhost:8000/todos
    HTTP/1.1 200 OK
    Content-Length: 142
    Content-Type: application/json
    Date: Thu, 19 Oct 2017 23:46:53 GMT
    Server: BaseHTTP/0.3 Python/2.7.10

    [
        {
            "description": "My first Todo",
            "metadata": {},
            "state": "unstarted",
            "uid": "8cc673f0-7dd3-4e9d-a20b-245fcd34859d",
            "username": "default"
        }
    ]


Now use the returned ID ``8cc673f0-7dd3-4e9d-a20b-245fcd34859d`` to delete
the specific Todo::

    $ http DELETE localhost:8000/todos/8cc673f0-7dd3-4e9d-a20b-245fcd34859d
    HTTP/1.1 200 OK
    Content-Length: 4
    Content-Type: application/json
    Date: Thu, 19 Oct 2017 23:57:32 GMT
    Server: BaseHTTP/0.3 Python/2.7.10

    null

Now if all of the Todo's are listed, it will no longer be present::

   $ http localhost:8000/todos
   HTTP/1.1 200 OK
   Content-Length: 2
   Content-Type: application/json
   Date: Thu, 19 Oct 2017 23:31:12 GMT
   Server: BaseHTTP/0.3 Python/2.7.10

   []


Add a route for updating the state of a specific Todo
-----------------------------------------------------

Add a route for updating the state of a specific Todo.

Instructions
~~~~~~~~~~~~

1. In the ``app.py``, add a function called ``update_todo()`` that accepts a
   ``uid`` as a parameter.

2. Decorate the ``update_todo()`` function with a ``route`` that only
   accepts ``PUT`` to the URI ``/todos/{uid}``.

3. In the ``update_todo()`` function use the ``app.current_request`` to update
   the Todo (which includes its description, metadata, and state) in the
   database for the ``uid`` provided.

.. literalinclude:: ../../../code/part1/02-add-chalicelib/app.py
   :linenos:
   :lines: 88-95


Verification
~~~~~~~~~~~~

To verify that the new route works, run ``chalice local`` and in a separate
terminal window run the following using ``httpie``::

   $ echo '{"description": "My first Todo", "metadata": {}}' | http POST localhost:8000/todos
   HTTP/1.1 200 OK
   Content-Length: 36
   Content-Type: application/json
   Date: Thu, 19 Oct 2017 23:44:24 GMT
   Server: BaseHTTP/0.3 Python/2.7.10

   de9a4981-f7fd-4639-97fb-2af247f20d79

Now determine the state of this newly added Todo::

    $ http localhost:8000/todos/de9a4981-f7fd-4639-97fb-2af247f20d79
    HTTP/1.1 200 OK
    Content-Length: 140
    Content-Type: application/json
    Date: Fri, 20 Oct 2017 00:03:26 GMT
    Server: BaseHTTP/0.3 Python/2.7.10

    {
        "description": "My first Todo",
        "metadata": {},
        "state": "unstarted",
        "uid": "de9a4981-f7fd-4639-97fb-2af247f20d79",
        "username": "default"
    }


Update the ``state`` of this Todo to ``started``::

    $ echo '{"state": "started"}' | http PUT localhost:8000/todos/de9a4981-f7fd-4639-97fb-2af247f20d79
    HTTP/1.1 200 OK
    Content-Length: 4
    Content-Type: application/json
    Date: Fri, 20 Oct 2017 00:05:07 GMT
    Server: BaseHTTP/0.3 Python/2.7.10

    null


Ensure that the Todo has the ``started`` state when described::

    $ http localhost:8000/todos/de9a4981-f7fd-4639-97fb-2af247f20d79
    HTTP/1.1 200 OK
    Content-Length: 138
    Content-Type: application/json
    Date: Fri, 20 Oct 2017 00:05:54 GMT
    Server: BaseHTTP/0.3 Python/2.7.10

    {
        "description": "My first Todo",
        "metadata": {},
        "state": "started",
        "uid": "de9a4981-f7fd-4639-97fb-2af247f20d79",
        "username": "default"
    }

Final Code
----------

When you are done your final code should look like this:

.. literalinclude:: ../../../code/part1/02-add-chalicelib/app.py
   :linenos:
   :lines: 1-95
