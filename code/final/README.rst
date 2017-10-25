===========
My Todo App
===========

This sample app lets you manage a Todo list.
It lets you create a new todo list as well as
check off existing todo items.


Design Overview
===============

Here's the REST API:

* GET    - /todos/ - Gets a list of all todo items
* POST   - /todos/ - Creates a new Todo item
* GET    - /todos/{id} - Gets a specific todo item
* DELETE - /todos/{id} - Deletes a specific todo item
* PUT    - /todos/{id} - Updates the state of a todo item

A todo item has this schema::

  {
    "description": {"type": "str"},
    "uid": {"type: "str"},
    "state": {"type: "str", "enum": ["unstarted", "started", "completed"]},
    "metadata": {
      "type": "object"
    }
  }


Dev Guide
=========

To run the tests::

    $ pip install ../../requirements-test.txt
    $ PYTHONPATH=. py.test tests/

To run the integration tests (which will make calls to dynamodb)::

    $ RUN_INTEG_TESTS=yes PYTHONPATH=. py.test tests/test_db.py

To run the app with dynamodb, there's a script that creates the table
and adds it to ``.chalice/config.json``::

    $ python createtable.py
    $ chalice local


Working With Users
==================

If you want to mess around with users, you need to create
the Users dynamodb table and create some test users.  You can
use the ``users.py`` script to help with this::

    # Create Users table and save it to config.json
    $ python createtable.py --table-type users --stage dev

    # Create a test user:
    $ python users.py --create-user
    Username: myusername
    Password:

    # To test that password verification works:
    $ python users.py -t
    Username: myusername
    Password:
    Password verified.


Testing Authentication
======================

First POST to /login::

    $ echo '{"username": "james", "password": "mypassword"}' | \
        http POST localhost:8000/login
    {
        "token": "...some long JWT token...",
    }

Now use that token as the Authorization header in subsequent requests::

    $ http GET localhost:8000/todos 'Authorization: ...some long JWT token...'
