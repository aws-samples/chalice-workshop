Section 0: Introduction to AWS Chalice
======================================

This section will provide an introduction on how to use AWS Chalice and provide
instructions on how to go about building your very first Chalice application.


Create a virtualenv and install Chalice
---------------------------------------

To start using Chalice, you will need a new virtualenv with Chalice installed.


Instructions
~~~~~~~~~~~~

Make sure you have Python 3 installed.  See the :doc:`env-setup` page for
instructions on how to install Python.

1) Create a new virtualenv called ``chalice-env`` by running the following
   command::

       $ python3 -m venv chalice-env


2) Activate your newly created virtualenv::

       $ source chalice-env/bin/activate


   If you are using a Windows environment, you will have to run::

       > .\chalice-env\Scripts\activate


3) Install ``chalice`` using ``pip``::

       $ pip install chalice


Verification
~~~~~~~~~~~~

To check that ``chalice`` was installed, run::

    $ chalice --version


This should print out the version of ``chalice`` that is installed in your
virtualenv.

Also, ensure that Python 3.7 is being used as the Python interpreter for your
virtualenv::

    $ python --version
    Python 3.7.3


Create a new Chalice application
---------------------------------

With ``chalice`` now installed, it is time to create your first Chalice
application.


Instructions
~~~~~~~~~~~~

1) Run the ``chalice new-project`` command to create a project called
   ``workshop-intro``::

       $ chalice new-project workshop-intro


Verification
~~~~~~~~~~~~

A new ``workshop-intro`` directory should have been created on your behalf.
Inside of the ``workshop-intro`` directory, you should have two files: an
``app.py`` file and a ``requirements.txt`` file::


   $ ls workshop-intro
   app.py           requirements.txt



Deploy the Chalice application
------------------------------

The newly created Chalice application can also be immediately deployed. So
let's deploy it.


Instructions
~~~~~~~~~~~~

1) Change directories to your newly created ``workshop-intro`` directory::

       $ cd workshop-intro


2) Run ``chalice deploy`` to deploy your Chalice application::

    $ chalice deploy
    Creating deployment package.
    Creating IAM role: workshop-intro-dev
    Creating lambda function: workshop-intro-dev
    Creating Rest API
    Resources deployed:
      - Lambda ARN: arn:aws:lambda:us-west-2:12345:function:workshop-intro-dev
      - Rest API URL: https://1y2mueb824.execute-api.us-west-2.amazonaws.com/api/


Verification
~~~~~~~~~~~~

The ``chalice deploy`` command should have exited with a return code of ``0``::

    $ echo $?
    0


You should also be able to interact with your newly deployed API. To do so,
first install ``httpie``::

    $ pip install httpie


Get the endpoint of your deployed Chalice application with ``chalice url``::

    $ chalice url
    https://1y2mueb824.execute-api.us-west-2.amazonaws.com/api/


Now use ``httpie`` to make an HTTP request to that endpoint::

    $ http https://1y2mueb824.execute-api.us-west-2.amazonaws.com/api/
    HTTP/1.1 200 OK
    Connection: keep-alive
    Content-Length: 18
    Content-Type: application/json
    Date: Sat, 21 Oct 2017 23:21:41 GMT
    Via: 1.1 403d925786ea6bd8903b99a628977c8f.cloudfront.net (CloudFront)
    X-Amz-Cf-Id: FlL4RfE3UqiDFocyTlSzCqtvzxWd9pK0M1lCnIsO1KwjhF37XvVTCg==
    X-Amzn-Trace-Id: sampled=0;root=1-59ebd683-72e3a6105ff3425da0c7e0ae
    X-Cache: Miss from cloudfront
    x-amzn-RequestId: 9776fca3-b6b6-11e7-94e4-b130a115985d

    {
        "hello": "world"
    }


The HTTP response back should consist of the JSON body: ``{"hello": "world"}``


Add a new route
---------------

Now that we have deployed our first Chalice application, let's expand on it
by adding a new ``/hello`` route.


Instructions
~~~~~~~~~~~~

1) Open the ``app.py`` file in your favorite editor::

       $ vim app.py


2) Inside of the ``app.py`` file, add the following function under the
   existing ``index()`` function::

        @app.route('/hello')
        def hello_workshop():
            return {'hello': 'workshop'}


   Your ``app.py`` should now consist of the following::

        from chalice import Chalice

        app = Chalice(app_name='workshop-intro')


        @app.route('/')
        def index():
            return {'hello': 'world'}

        @app.route('/hello')
        def hello_workshop():
            return {'hello': 'workshop'}


3) Deploy the updated application using ``chalice deploy``::

        $ chalice deploy
        Creating deployment package.
        Updating policy for IAM role: workshop-intro-dev
        Updating lambda function: workshop-intro-dev
        Updating rest API
        Resources deployed:
          - Lambda ARN: arn:aws:lambda:us-west-2:12345:function:workshop-intro-dev
          - Rest API URL: https://1y2mueb824.execute-api.us-west-2.amazonaws.com/api/


Validation
~~~~~~~~~~

Using ``httpie``, confirm that the new route was deployed by making an
HTTP request::

    $ http https://1y2mueb824.execute-api.us-west-2.amazonaws.com/api/hello
    HTTP/1.1 200 OK
    Connection: keep-alive
    Content-Length: 21
    Content-Type: application/json
    Date: Sat, 21 Oct 2017 23:34:56 GMT
    Via: 1.1 2d8af5cc5befc5d35bb54b4a5b6494c9.cloudfront.net (CloudFront)
    X-Amz-Cf-Id: upMVSIUvjmCRa33IO-4zpYQOU0C94h50F3oJX_iv-vdk-g1IacKq9A==
    X-Amzn-Trace-Id: sampled=0;root=1-59ebd9a0-0a275c8f6794f2e5c59641c7
    X-Cache: Miss from cloudfront
    x-amzn-RequestId: 7233e21a-b6b8-11e7-a3b6-f7221d70ee14

    {
        "hello": "workshop"
    }

The HTTP response back should consist of the JSON body:
``{"hello": "workshop"}``



Add a new route with a URI parameter
------------------------------------

Next, let's add a new route that accepts a parameter in the URI.

Instructions
~~~~~~~~~~~~

1) Inside of the ``app.py`` file, add the following function under the
   existing ``hello_workshop()`` function::

        @app.route('/hello/{name}')
        def hello_name(name):
            return {'hello': name}


   Your ``app.py`` should now consist of the following::

        from chalice import Chalice

        app = Chalice(app_name='workshop-intro')


        @app.route('/')
        def index():
            return {'hello': 'world'}

        @app.route('/hello')
        def hello_workshop():
            return {'hello': 'workshop'}

        @app.route('/hello/{name}')
        def hello_name(name):
            return {'hello': name}


2) Deploy the updated application using ``chalice deploy``::

        $ chalice deploy
        Creating deployment package.
        Updating policy for IAM role: workshop-intro-dev
        Updating lambda function: workshop-intro-dev
        Updating rest API
        Resources deployed:
          - Lambda ARN: arn:aws:lambda:us-west-2:12345:function:workshop-intro-dev
          - Rest API URL: https://1y2mueb824.execute-api.us-west-2.amazonaws.com/api/


Verification
~~~~~~~~~~~~

Using ``httpie``, confirm that the new route was deployed by making an
HTTP request::

    $ http https://1y2mueb824.execute-api.us-west-2.amazonaws.com/api/hello/kyle
    HTTP/1.1 200 OK
    Connection: keep-alive
    Content-Length: 21
    Content-Type: application/json
    Date: Sat, 21 Oct 2017 23:34:56 GMT
    Via: 1.1 2d8af5cc5befc5d35bb54b4a5b6494c9.cloudfront.net (CloudFront)
    X-Amz-Cf-Id: upMVSIUvjmCRa33IO-4zpYQOU0C94h50F3oJX_iv-vdk-g1IacKq9A==
    X-Amzn-Trace-Id: sampled=0;root=1-59ebd9a0-0a275c8f6794f2e5c59641c7
    X-Cache: Miss from cloudfront
    x-amzn-RequestId: 7233e21a-b6b8-11e7-a3b6-f7221d70ee14

    {
        "hello": "kyle"
    }


The HTTP response back should consist of the JSON body:
``{"hello": "kyle"}``


Add a new route with a non-GET HTTP method
------------------------------------------

For our last route, let's add a new route that accepts a different HTTP method
other than ``GET``.


Instructions
~~~~~~~~~~~~

1) Inside of the ``app.py`` file, add the following function under the
   existing ``hello_name()`` function::

        @app.route('/hello-post', methods=['POST'])
        def hello_post():
            request_body = app.current_request.json_body
            return {'hello': request_body}


   Your ``app.py`` should now consist of the following::

        from chalice import Chalice

        app = Chalice(app_name='workshop-intro')


        @app.route('/')
        def index():
            return {'hello': 'world'}

        @app.route('/hello')
        def hello_workshop():
            return {'hello': 'workshop'}

        @app.route('/hello/{name}')
        def hello_name(name):
            return {'hello': name}

        @app.route('/hello-post', methods=['POST'])
        def hello_post():
            request_body = app.current_request.json_body
            return {'hello': request_body}


2) Deploy the updated application using ``chalice deploy``::

        $ chalice deploy
        Creating deployment package.
        Updating policy for IAM role: workshop-intro-dev
        Updating lambda function: workshop-intro-dev
        Updating rest API
        Resources deployed:
          - Lambda ARN: arn:aws:lambda:us-west-2:12345:function:workshop-intro-dev
          - Rest API URL: https://1y2mueb824.execute-api.us-west-2.amazonaws.com/api/


Verification
~~~~~~~~~~~~

Using ``httpie``, confirm that the new route was deployed by making an
HTTP request::

    $ echo '{"request":"body"}' | http POST https://1y2mueb824.execute-api.us-west-2.amazonaws.com/api/hello-post
    HTTP/1.1 200 OK
    Connection: keep-alive
    Content-Length: 30
    Content-Type: application/json
    Date: Sat, 21 Oct 2017 23:48:43 GMT
    Via: 1.1 805232684895bb3db77c2db44011c8d0.cloudfront.net (CloudFront)
    X-Amz-Cf-Id: ah7w7to9Svn_WzGZ1MldMHERCO_sLxMKQi9AcHFLSjLtAdAPhw5z_A==
    X-Amzn-Trace-Id: sampled=0;root=1-59ebdcdb-32c834bbd0341b40e3dfd787
    X-Cache: Miss from cloudfront
    x-amzn-RequestId: 5f0bf184-b6ba-11e7-a22d-9b7d2bcfb95b

    {
        "hello": {
            "request": "body"
        }
    }

Notice the HTTP response back should contain the JSON blob that was echoed
into standard input.


Delete the Chalice application
------------------------------

Now with an understanding of the basics of how to use AWS Chalice, let's
clean up this introduction application by deleting it remotely.


Instructions
~~~~~~~~~~~~

1) Run ``chalice delete`` to delete the deployed AWS resources running this
   application::

        $ chalice delete
        Deleting Rest API: 1y2mueb824
        Deleting function: arn:aws:lambda:us-west-2:12345:function:workshop-intro-dev
        Deleting IAM role: workshop-intro-dev

   If you are prompted on whether to delete a resource when deleting the
   application, go ahead and confirm by entering ``y``.


Verification
~~~~~~~~~~~~

To ensure that the API no longer exists remotely, try to make an HTTP request
to the endpoint it was originally deployed to::

    $ http https://1y2mueb824.execute-api.us-west-2.amazonaws.com/api/

    http: error: SSLError: [SSL: SSLV3_ALERT_HANDSHAKE_FAILURE] sslv3 alert
    handshake failure (_ssl.c:590) while doing GET request to URL:
    https://1y2mueb824.execute-api.us-west-2.amazonaws.com/api/


This should result in an SSL error as the remote application no longer exists
and therefore it cannot be connected to it.
