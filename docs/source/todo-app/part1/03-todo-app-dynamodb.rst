Section 3: Add a DynamoDB table for Todo application
====================================================


In this step, we'll replace the in-memory database with an
Amazon DynamoDB table.


Initial Setup
-------------

The starting code for this step is in the ``chalice-workshop/code/todo-app/part1/03-add-dynamodb``
file.  If necessary, you can copy over those files as a starting point
for this step::

    $ cp ../chalice-workshop/code/todo-app/part1/03-add-dynamodb/app.py app.py
    $ cp ../chalice-workshop/code/todo-app/part1/03-add-dynamodb/createtable.py createtable.py
    $ cp ../chalice-workshop/code/todo-app/part1/03-add-dynamodb/chalicelib/db.py chalicelib/db.py
    $ cp ../chalice-workshop/code/todo-app/part1/03-add-dynamodb/.chalice/policy-dev.json .chalice/policy-dev.json
    $ cp ../chalice-workshop/code/todo-app/part1/03-add-dynamodb/.chalice/config.json .chalice/config.json


Create a DynamoDB table
------------------------

In this section, we're going to create a DynamoDB table and
configure chalice to pass in the table name to our application.

1. First, we'll need to install boto3, the AWS SDK for Python.
   Run this command::

    $ pip install boto3

2. Add boto3 to our requirements.txt file.
   Chalice uses this file when building the deployment package
   for your app::

    $ pip freeze | grep boto3 >> requirements.txt

3. Now that boto3 is installed, we can create the DynamoDB table
   Run the ``createtable.py`` script with the ``--table-type app`` option.
   This will take a few seconds to run. ::

    $ python createtable.py --table-type app


5. Verify that this script added the table name to the ``.chalice/config.json``
   file.  You should see a key named ``APP_TABLE_NAME`` in this file::

    $ cat .chalice/config.json
    {
      "stages": {
        "dev": {
          "environment_variables": {
            "APP_TABLE_NAME": "todo-app-...."
          },
          "api_gateway_stage": "api"
        }
      },
      "version": "2.0",
      "app_name": "testapp"
    }

6. Next, we'll add a test route to double check we've configured
   everything correctly.  Open the ``app.py`` file and these import
   lines to the top of the file::

       import os
       import boto3

7. Add a new test route:

  .. code-block:: python

      @app.route('/test-ddb')
      def test_ddb():
          resource = boto3.resource('dynamodb')
          table = resource.Table(os.environ['APP_TABLE_NAME'])
          return table.name


Verification
~~~~~~~~~~~~

1. Start up the local dev server: ``chalice local``
2. Make a request to this test route and verify you get a 200 response::

    $ http localhost:8000/test-ddb
    HTTP/1.1 200 OK
    Content-Length: 45
    Content-Type: application/json
    Server: BaseHTTP/0.3 Python/2.7.14

    todo-app-0b116e7b-f0f8-4548-91d8-95c75898b8b6


Switching the ``InMemoryTodoDB`` to a ``DynamoDBTodo``
------------------------------------------------------

Now that we've verified our DynamoDB table is plumbed into our
chalice app correctly, we can update to use a new ``DynamoDBTodo``
backend instead of the ``InMemoryTodoDB``.

The ``chalicelib/db.py`` file you copied from
``code/todo-app/part1/03-add-dynamodb/chalicelib/db.py`` has a new ``DynamoDBTodo``
class.  This has the same interface as ``InMemoryTodoDB`` except that is uses
DynamoDB as the backend.  We're going to update our ``app.py`` to use this new
class.

1. Remove the ``@app.route('/test-ddb')`` view function.  We
   no longer need it now that we've verified that DynamoDB is correctly
   configured for our app.

2. Go to the ``get_app_db()`` function in your ``app.py`` file.  Modify
   this function to use the ``DynamoDBTodo`` backend:

    .. code-block:: python

        def get_app_db():
            global _DB
            if _DB is None:
                _DB = db.DynamoDBTodo(
                    boto3.resource('dynamodb').Table(
                        os.environ['APP_TABLE_NAME'])
                )
            return _DB

3. Go to the top of the ``app.py`` file. Modify the line ``from chalicelib.db import InMemoryTodoDB`` to reference ``db`` instead:
 
    .. code-block:: python

        from chalicelib import db

Verification
~~~~~~~~~~~~

1. Start up the local dev server ``chalice local``

2. Create a Todo item::

    $ echo '{"description": "My first Todo", "metadata": {}}' | \
        http POST localhost:8000/todos
    HTTP/1.1 200 OK
    Content-Length: 36
    Content-Type: application/json
    Date: Thu, 19 Oct 2017 23:44:24 GMT
    Server: BaseHTTP/0.3 Python/2.7.10

    de9a4981-f7fd-4639-97fb-2af247f20d79

3. Retrieve the Todo item you just created.  Keep in mind that your UID will be
   different from what's shown below::

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

Deploy your app
---------------

1. Now that we've tested locally, we're ready to deploy::

    $ chalice deploy

Verification
~~~~~~~~~~~~

1. First create a Todo item using the API Gateway endpoint::

    $ chalice url
    https://your-chalice-url/
    $ echo '{"description": "My second Todo", "metadata": {}}' | \
        http POST https://your-chalice-url/todos
    HTTP/1.1 200 OK
    Content-Length: 36
    Content-Type: application/json

    abcdefg-abcdefg

2. Verify you can retrieve this item::

    $ http https://your-chalice-url/todos/abcdefg-abcdefg
    HTTP/1.1 200 OK
    Content-Length: 140
    Content-Type: application/json

    {
        "description": "My second Todo",
        "metadata": {},
        "state": "unstarted",
        "uid": "abcdefg-abcdefg",
        "username": "default"
    }
