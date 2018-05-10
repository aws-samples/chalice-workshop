Section 4: Add authorization to Todo application
================================================

If you had noticed from the previous steps, there was a ``username`` field
for all of the Todos, but the ``username`` was always set to ``default``.
This step will be utilizing the ``username`` field by exposing the notion
of users and authorization in the Todo application.  For this section, we will
be doing the following to add authorization and users to the application:

.. contents::
   :local:
   :depth: 1


Install PyJWT
-------------

For authorization, the application is going to be relying on JWT. To depend
on JWT, in the Chalice application ``PyJWT`` needs to be installed and added
to our ``requirements.txt`` file.


Instructions
~~~~~~~~~~~~

1) Add ``PyJWT`` to your ``requirements.txt`` file::

       $ echo PyJWT==1.6.1 >> requirements.txt


2) Make sure it is now installed in your virtualenv::

       $ pip install -r requirements.txt


Verification
~~~~~~~~~~~~

To ensure that it was installed, open the Python REPL and try to import
the ``PyJWT`` library::

   $ python
     Python 2.7.10 (default, Mar 10 2016, 09:55:31)
     [GCC 4.2.1 Compatible Apple LLVM 7.0.2 (clang-700.1.81)] on darwin
     Type "help", "copyright", "credits" or "license" for more information.
     >>> import jwt


Copy over auth specific files
-----------------------------

In order to add authentication to your Chalice application we have provided a few
files that help with some of the low-level details. We have added an ``auth.py`` file
to ``chalicelib`` which abstracts away some of the details of handling JWT tokens. We
have also added a ``users.py`` script which is a command line utility for creating and
managing a user table.


Instructions
~~~~~~~~~~~~

1) Copy in the ``chalice-workshop/code/part1/04-add-auth/chalicelib/auth.py``
file::

       $ cp ../chalice-workshop/code/part1/04-add-auth/chalicelib/auth.py chalicelib/auth.py


2) Copy over the ``chalice-workshop/code/part1/04-add-auth/users.py`` script for
creating users::

       $ cp ../chalice-workshop/code/part1/04-add-auth/users.py users.py



Verification
~~~~~~~~~~~~

From within the ``mytodo`` directory of your Todo Chalice application, the
structure should be the following::

    $ tree
    .
    ├── app.py
    ├── chalicelib
    │   ├── __init__.py
    │   ├── auth.py
    │   └── db.py
    ├── createtable.py
    ├── requirements.txt
    └── users.py


Create a DynamoDB user table
----------------------------

Using the ``createtable.py`` script, this will create another DynamoDB table
for storing users to use in the Chalice application.

Instructions
~~~~~~~~~~~~

1) Run the ``createtable.py`` script to create the DynamoDB table::

      $ python createtable.py -t users


Verification
~~~~~~~~~~~~

Check that the return code of the command is ``0``::

    $ echo $?
    0


Also ``cat`` the ``.chalice/config.json`` to make sure the ``USERS_TABLE_NAME``
shows up as an environment variable::

    $ cat .chalice/config.json
    {
      "stages": {
        "dev": {
          "environment_variables": {
            "USERS_TABLE_NAME": "users-app-21658b12-517e-4441-baef-99b8fc2f0b61",
            "APP_TABLE_NAME": "todo-app-323ca4c3-54fb-4e49-a584-c52625e5d85d"
          },
          "autogen_policy": false,
          "api_gateway_stage": "api"
        }
      },
      "version": "2.0",
      "app_name": "mytodo"
    }


Add a user to the user table
----------------------------

Using the ``users.py`` script, create a new user in your users database to
use with your chalice application.

Instructions
~~~~~~~~~~~~

1) Run the ``users.py`` script with the ``-c`` argument to create a user. You
   will be prompted for a username and a password::


    $ python users.py -c
    Username: user
    Password:


Verification
~~~~~~~~~~~~

Using the ``users.py`` script, make sure that the user is listed in your
database::

    $ python users.py -l
    user


Also make sure that the password is correct by testing the username and
password with the ``users.py`` script::

    $ python users.py -t
    Username: user
    Password:
    Password verified.

You can also test an incorrect password.  You should see this output::

    $ python users.py -t
    Username: user
    Password:
    Password verification failed.


Create ``get_users_db`` function
--------------------------------

Now that we have created a DynamoDB user table, we will create a convenience function
for loading it.

Instructions
~~~~~~~~~~~~

1. Add a new variable ``_USER_DB`` in your ``app.py`` file with a value of None:


.. code-block:: python

    app = Chalice(app_name='mytodo')
    app.debug = True
    _DB = None
    # This is the new value you're adding.
    _USER_DB = None


2. Create a function for fetching our current database table for users. Similar to the
   function that gets the app table.  Add this function to your ``app.py`` file:


.. literalinclude:: ../../../code/final/app.py
   :linenos:
   :lines: 31-36


Create a login route
--------------------

We will now create a login route where users can trade their username/password for a
JWT token.


Instructions
~~~~~~~~~~~~

1. Define a new Chalice route ``/login`` that accepts the POST method and grabs the
   ``username`` and ``password`` from the request, and forwards it along to a helper
   function in the ``auth`` code you copied in earlier which will trade those for a
   JWT token.

.. literalinclude:: ../../../code/final/app.py
   :linenos:
   :lines: 14-21

2. Notice the above code snippit uses the ``auth`` file that we copied into our
   chalicelib directory at the beginning of this step. Add the following
   import statement to the top of ``app.py`` so we can use it::

    from chalicelib import auth


Verification
~~~~~~~~~~~~

1. Start up a local server using ``chalice local``.

2. Using the username and password generated previously, run ``chalice local``
   and make an HTTP ``POST`` request to the ``/login`` URI::

    $ echo '{"username": "user", "password": "password"}' | \
        http POST localhost:8000/login
    HTTP/1.1 200 OK
    Content-Length: 218
    Content-Type: application/json
    Date: Fri, 20 Oct 2017 22:48:42 GMT
    Server: BaseHTTP/0.3 Python/2.7.10

    {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE1MDg1Mzk3MjIsImp0aSI6IjI5ZDJhNmFkLTdlY2YtNDYzZC1iOTY1LTk0M2VhNzU0YWMzYyIsInN1YiI6InVzZXIiLCJuYmYiOjE1MDg1Mzk3MjJ9.95hlpRWARK95aYCh0YE7ls_cvraoenNux8gmIy8vQU8"
    }


This should return a JWT to use as an ``Authorization`` header for that user.


Create a custom authorizer and attach to a route
------------------------------------------------

To add authorization to our app we will start by defining an authorizer and
attaching it to one of our routes.


Instructions
~~~~~~~~~~~~

1. Create an authorizer function that checks the validity of a JWT token using the
   existing code in the ``auth.py`` file we copied earlier. If the token is valid
   (didn't throw an error) we will return a policy that allows access to all of our
   routes, and sets the ``principal_id`` to the username in the JWT token.

2. Once we have defined the authorizer, we will attach it to the ``get_todos`` route.

.. literalinclude:: ../../../code/final/app.py
   :linenos:
   :lines: 24-28

.. literalinclude:: ../../../code/final/app.py
   :linenos:
   :lines: 56-57


Also make sure to import the ``AuthResponse`` class at the top of the ``app.py`` file:

.. code-block:: python

    from chalice import AuthResponse


Verification
~~~~~~~~~~~~

1. Start the local dev server ``chalice local``


2. Try to get the todo, the request should be rejected without authorization::

    $ http localhost:8000/todos
    HTTP/1.1 401 Unauthorized
    Content-Length: 26
    Content-Type: application/json
    Date: Tue, 24 Oct 2017 02:50:50 GMT
    Server: BaseHTTP/0.3 Python/2.7.13
    x-amzn-ErrorType: UnauthorizedException
    x-amzn-RequestId: 297d1da8-b9a8-4824-a1f3-293607aac715

    {
	"message": "Unauthorized"
    }

3. Try the same call again but with your authorization token passed in the
   ``Authorization`` header::


    $ http localhost:8000/todos \
        Authorization:eyJhbGciOi.... really long token here...
    Content-Length: 137
    Content-Type: application/json
    Date: Tue, 24 Oct 2017 02:50:43 GMT
    Server: BaseHTTP/0.3 Python/2.7.13

    [
	{
	    "description": "My first Todo",
	    "metadata": {},
	    "state": "unstarted",
	    "uid": "f9a992d6-41c0-45a6-84b8-e7239f7d7100",
	    "username": "john"
	}
    ]

Attach authorizer to the rest of the routes
-------------------------------------------

Now attach the authorizer to all the other routes except the ``login`` route.

Instructions
~~~~~~~~~~~~

1. Attach the ``jwt_auth`` authorizer to the ``add_new_todo`` route.

2. Attach the ``jwt_auth`` authorizer to the ``get_todo`` route.

3. Attach the ``jwt_auth`` authorizer to the ``delete_todo`` route.

4. Attach the ``jwt_auth`` authorizer to the ``update_todo`` route.


.. literalinclude:: ../../../code/final/app.py
   :linenos:
   :lines: 62-63

.. literalinclude:: ../../../code/final/app.py
   :linenos:
   :lines: 73-74

.. literalinclude:: ../../../code/final/app.py
   :linenos:
   :lines: 79-80

.. literalinclude:: ../../../code/final/app.py
   :linenos:
   :lines: 85-86

Verification
~~~~~~~~~~~~

1. Start up the local dev server ``chalice local``

2. Try each route without an authorization token. You should get a ``401``
   Unauthorized response::

    $ echo '{"description": "My first Todo", "metadata": {}}' | \
        http POST localhost:8000/todos
    HTTP/1.1 401 Unauthorized
    Content-Length: 26
    Content-Type: application/json
    Date: Tue, 24 Oct 2017 03:14:14 GMT
    Server: BaseHTTP/0.3 Python/2.7.13
    x-amzn-ErrorType: UnauthorizedException
    x-amzn-RequestId: 58c2d520-07e6-4535-b034-aaba41bab8ab

    {
	"message": "Unauthorized"
    }

  ::

    $ http GET localhost:8000/todos/fake-id
    HTTP/1.1 401 Unauthorized
    Content-Length: 26
    Content-Type: application/json
    Date: Tue, 24 Oct 2017 03:15:10 GMT
    Server: BaseHTTP/0.3 Python/2.7.13
    x-amzn-ErrorType: UnauthorizedException
    x-amzn-RequestId: b2304a70-ff8d-453f-b119-10e75326463a

    {
	"message": "Unauthorized"
    }

  ::

    $ http DELETE localhost:8000/todos/fake-id
    HTTP/1.1 401 Unauthorized
    Content-Length: 26
    Content-Type: application/json
    Date: Tue, 24 Oct 2017 03:17:10 GMT
    Server: BaseHTTP/0.3 Python/2.7.13
    x-amzn-ErrorType: UnauthorizedException
    x-amzn-RequestId: 69419241-b244-462b-b108-72091f7d7b5b

    {
	"message": "Unauthorized"
    }

  ::

    $ echo '{"state": "started"}' | http PUT localhost:8000/todos/fake-id
    HTTP/1.1 401 Unauthorized
    Content-Length: 26
    Content-Type: application/json
    Date: Tue, 24 Oct 2017 03:18:59 GMT
    Server: BaseHTTP/0.3 Python/2.7.13
    x-amzn-ErrorType: UnauthorizedException
    x-amzn-RequestId: edc77f3d-3d3d-4a29-850a-502f21aeed96

    {
	"message": "Unauthorized"
    }

3. Now try to create, get, update, and delete a todo from your application by
   using the ``Authorization`` header in all your requests::

     $ echo '{"description": "My first Todo", "metadata": {}}' | \
          http POST localhost:8000/todos Authorization:eyJhbG... auth token ...
     HTTP/1.1 200 OK
     Content-Length: 36
     Content-Type: application/json
     Date: Tue, 24 Oct 2017 03:24:28 GMT
     Server: BaseHTTP/0.3 Python/2.7.13

     93dbabdb-3b2f-4029-845b-7754406c494f

  ::

     $ echo '{"state": "started"}' | \
         http PUT localhost:8000/todos/93dbabdb-3b2f-4029-845b-7754406c494f \
	 Authorization:eyJhbG... auth token ...
     HTTP/1.1 200 OK
     Content-Length: 4
     Content-Type: application/json
     Date: Tue, 24 Oct 2017 03:25:28 GMT
     Server: BaseHTTP/0.3 Python/2.7.13

     null

  ::

     $ http localhost:8000/todos/93dbabdb-3b2f-4029-845b-7754406c494f \
         Authorization:eyJhbG... auth token ...
     HTTP/1.1 200 OK
     Content-Length: 135
     Content-Type: application/json
     Date: Tue, 24 Oct 2017 03:26:29 GMT
     Server: BaseHTTP/0.3 Python/2.7.13

     {
	 "description": "My first Todo",
	 "metadata": {},
	 "state": "started",
	 "uid": "93dbabdb-3b2f-4029-845b-7754406c494f",
	 "username": "default"
     }

  ::

     $ http DELETE localhost:8000/todos/93dbabdb-3b2f-4029-845b-7754406c494f \
         Authorization:eyJhbG... auth token ...
     HTTP/1.1 200 OK
     Content-Length: 4
     Content-Type: application/json
     Date: Tue, 24 Oct 2017 03:27:10 GMT
     Server: BaseHTTP/0.3 Python/2.7.13

     null

Use authorizer provided username
--------------------------------

Now that we have authorizers hooked up to all our routes we can use that
instead of relying on the default user of ``default``.

Instructions
~~~~~~~~~~~~

1. First create a function named ``get_authorized_username`` that will be used
   to convert the information we have in our ``current_request`` into a
   username.

.. literalinclude:: ../../../code/final/app.py
   :linenos:
   :lines: 52-53

2. Now we need to update each function that interacts with our database to
   calculate the ``username`` and pass it to the ``xxx_item`` method.

.. literalinclude:: ../../../code/final/app.py
   :linenos:
   :lines: 56-94
   :emphasize-lines: 3,4,10,12,20,21,26,27,33,39

Verification
~~~~~~~~~~~~

1. Spin up the local Chalice server with ``chalice local``.

2. Create a new todo and pass in your auth token::

     $ echo '{"description": "a todo", "metadata": {}}' | \
          http POST localhost:8000/todos Authorization:eyJhbG... auth token ...
     HTTP/1.1 200 OK
     Content-Length: 36
     Content-Type: application/json
     Date: Tue, 24 Oct 2017 04:16:57 GMT
     Server: BaseHTTP/0.3 Python/2.7.13

     71048cc2-8583-41e5-9dfe-b9669d15af7d

3. List your todos using the get_todos route::

     $ http localhost:8000/todos Authorization:eyJhbG... auth token ...
     HTTP/1.1 200 OK
     Content-Length: 132
     Content-Type: application/json
     Date: Tue, 24 Oct 2017 04:21:58 GMT
     Server: BaseHTTP/0.3 Python/2.7.13

     [
	 {
	     "description": "a todo",
	     "metadata": {},
	     "state": "unstarted",
	     "uid": "7212a932-769b-4a19-9531-a950db7006a5",
	     "username": "john"
	 }
     ]

4. Notice that now the username is no longer ``default`` it should be whatever username
   went with the auth token you supplied.

5. Try making a new user with ``python users.py -c`` and then get their JWT token
   by calling the login route with their credentials.

6. Call the same route as above as the new user by passing in their JWT token in the
   ``Authorization`` header. They should get no todos since they have not created any
   yet::

     http localhost:8000/todos 'Authorization:...the other auth token...'
     HTTP/1.1 200 OK
     Content-Length: 2
     Content-Type: application/json
     Date: Tue, 24 Oct 2017 04:25:56 GMT
     Server: BaseHTTP/0.3 Python/2.7.13

     []


Deploying your authorizer code
------------------------------

Now that we have it working locally lets deploy it and verify that it still works.

Instructions
~~~~~~~~~~~~

1. ``chalice deploy`` your app.

Verification
~~~~~~~~~~~~

1. Try the same two calls above against the real API Gateway endpoint you get from your
   deploy instead of the localhost endpoint. If you lose your endpoint you can run
   ``chalice url`` which will print out your API Gateway endpoint::

     $ http <your endpoint here>/todos Authorization:http localhost:8000/todos \
         'Authorization:...auth token that has no todos...'
     HTTP/1.1 200 OK
     Connection: keep-alive
     Content-Length: 2
     Content-Type: application/json
     Date: Tue, 24 Oct 2017 04:43:20 GMT
     Via: 1.1 cff9911a0035fa608bcaa4e9709161b3.cloudfront.net (CloudFront)
     X-Amz-Cf-Id: bunfoZShHff_f3AqBPS2d5Ae3ymqgBusANDP9G6NvAZB3gOfr1IsVA==
     X-Amzn-Trace-Id: sampled=0;root=1-59f01668-388cc9fa3db607662c2d623c
     X-Cache: Miss from cloudfront
     x-amzn-RequestId: 06de2818-b93f-11e7-bbb0-b760b41808da

     []

  ::

     $ http <your endpoint here>/todos Authorization:http localhost:8000/todos \
         'Authorization:...auth token that has a todo...'
     HTTP/1.1 200 OK
     Connection: keep-alive
     Content-Length: 132
     Content-Type: application/json
     Date: Tue, 24 Oct 2017 04:43:45 GMT
     Via: 1.1 a05e153e17e2a6485edf7bf733e131a4.cloudfront.net (CloudFront)
     X-Amz-Cf-Id: wR_7Bp4KglDjF41_9TNxXmc3Oiu2kll5XS1sTCCP_LD1kMC3C-nqOA==
     X-Amzn-Trace-Id: sampled=0;root=1-59f01681-bb8ce2d74dc0c6f8fe095f9d
     X-Cache: Miss from cloudfront
     x-amzn-RequestId: 155f88f7-b93f-11e7-b351-775deacbeb7a

     [
	 {
	     "description": "a todo",
	     "metadata": {},
	     "state": "unstarted",
	     "uid": "7212a932-769b-4a19-9531-a950db7006a5",
	     "username": "john"
	 }
     ]



Final Code
----------

When you are finished your ``app.py`` file should look like:

.. literalinclude:: ../../../code/final/app.py
   :linenos:
   :lines: 1-94
