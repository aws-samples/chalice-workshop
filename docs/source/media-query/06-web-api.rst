Part 6: Add REST API to query media files
=========================================

So far we have been querying the image files stored in our table via the AWS
CLI. However, it would be more helpful to have an API on-top of the table
instead of having to query it directly with the AWS CLI. We will now use Amazon
API Gateway integrations with Lambda to create an API for our application.
This API will have two routes:

* ``GET /`` - List all media items in the table. You can supply the query
  string parameters: ``startswith``, ``media-type``, and ``label`` to further
  filter the media items returned in the API call

* ``GET /{name}`` - Retrieve the media item based on the ``name`` of the media
  item.


To create this API, we will perform the following steps:

.. contents::
   :local:
   :depth: 1

Add route for listing media items
---------------------------------

Add an API route ``GET /`` that lists all items in the table and allows
users to query on ``startswith``, ``media-type``, and ``label``.

Instructions
~~~~~~~~~~~~

1. In the ``app.py`` file, define the function ``list_media_files()`` that
   has the route ``GET /`` using the
   `app.route <https://chalice.readthedocs.io/en/latest/api.html#Chalice.route>`__
   decorator::

    @app.route('/')
    def list_media_files():


2. Inside of the ``list_media_files()`` function, extract the query string
   parameters from the
   `app.current_request <https://chalice.readthedocs.io/en/latest/api.html#Request>`__
   object and query the database for the media files:

   .. literalinclude:: ../../../code/media-query/07-videos/app.py
      :lines: 50-55,64-75


Verification
~~~~~~~~~~~~

1. Ensure the contents of the ``app.py`` file is:

.. literalinclude:: ../../../code/media-query/07-videos/app.py
   :linenos:
   :lines: 1-4,6-55,64-84

2. Install `HTTPie <https://httpie.org/>`__ to query the API::

    $ pip install httpie


3. In a different terminal, run ``chalice local`` to run the API as a server
   locally::

    $ chalice local

4. Use HTTPie to query the API for all images::

    $ http 127.0.0.1:8000/
    HTTP/1.1 200 OK
    Content-Length: 126
    Content-Type: application/json
    Date: Tue, 17 Jul 2018 13:59:35 GMT
    Server: BaseHTTP/0.6 Python/3.6.1

    [
        {
            "labels": [
                "Animal",
                "Canine",
                "Dog",
                "German Shepherd",
                "Mammal",
                "Pet",
                "Collie"
            ],
            "name": "sample.jpg",
            "type": "image"
        }
    ]


5. Use HTTPie to query the API using the query string parameter ``label``::

    $ http 127.0.0.1:8000/ label==Dog
    HTTP/1.1 200 OK
    Content-Length: 126
    Content-Type: application/json
    Date: Tue, 17 Jul 2018 14:01:22 GMT
    Server: BaseHTTP/0.6 Python/3.6.1

    [
        {
            "labels": [
                "Animal",
                "Canine",
                "Dog",
                "German Shepherd",
                "Mammal",
                "Pet",
                "Collie"
            ],
            "name": "sample.jpg",
            "type": "image"
        }
    ]
    $ http 127.0.0.1:8000/ label==Person
    HTTP/1.1 200 OK
    Content-Length: 2
    Content-Type: application/json
    Date: Tue, 17 Jul 2018 14:01:46 GMT
    Server: BaseHTTP/0.6 Python/3.6.1

    []

   Feel free to test out any of the other query string parameters as well.


Add route for retrieving a single media item
--------------------------------------------

Add an API route ``GET /{name}`` that retrieves a single item in the table
using the ``name`` of the item.

Instructions
~~~~~~~~~~~~

1. Import ``chalice.NotFoundError`` in the ``app.py`` file:

.. literalinclude:: ../../../code/media-query/07-videos/app.py
   :linenos:
   :lines: 1-7
   :emphasize-lines: 5

2. In the ``app.py`` file, define the function ``get_media_file()`` decorated
   by ``app.route('/{name}')``:

   .. literalinclude:: ../../../code/media-query/07-videos/app.py
      :lines: 58-59

3. Within the ``get_media_file()`` function, query the media item using the
   ``name`` parameter and raise a ``chalice.NotFoundError`` exception when the
   ``name`` does not exist in the database:

   .. literalinclude:: ../../../code/media-query/07-videos/app.py
      :lines: 58-63


Verification
~~~~~~~~~~~~

1. Ensure the contents of the ``app.py`` file is:

.. literalinclude:: ../../../code/media-query/07-videos/app.py
   :linenos:
   :lines: 1-84

2. If the local server is not still running, run ``chalice local`` to
   restart the local API server::

    $ chalice local


3. Use HTTPie to query the API for the ``sample.jpg`` image::

    $ http 127.0.0.1:8000/sample.jpg
    HTTP/1.1 200 OK
    Content-Length: 124
    Content-Type: application/json
    Date: Tue, 17 Jul 2018 14:09:01 GMT
    Server: BaseHTTP/0.6 Python/3.6.1

    {
        "labels": [
            "Animal",
            "Canine",
            "Dog",
            "German Shepherd",
            "Mammal",
            "Pet",
            "Collie"
        ],
        "name": "sample.jpg",
        "type": "image"
    }



4. Use HTTPie to query the API for an image that does not exist::

    $ http 127.0.0.1:8000/noexists.jpg
    HTTP/1.1 404 Not Found
    Content-Length: 90
    Content-Type: application/json
    Date: Tue, 17 Jul 2018 14:09:34 GMT
    Server: BaseHTTP/0.6 Python/3.6.1

    {
        "Code": "NotFoundError",
        "Message": "NotFoundError: Media file (noexists.jpg) not found"
    }


Redeploy the Chalice application
--------------------------------

Deploy the Chalice application based on the updates.

Instructions
~~~~~~~~~~~~

1. Run ``chalice deploy``::

    $ chalice deploy
    Creating deployment package.
    Updating policy for IAM role: media-query-dev-handle_object_created
    Updating lambda function: media-query-dev-handle_object_created
    Configuring S3 events in bucket media-query-mediabucket-fb8oddjbslv1 to function media-query-dev-handle_object_created
    Updating policy for IAM role: media-query-dev-handle_object_removed
    Updating lambda function: media-query-dev-handle_object_removed
    Configuring S3 events in bucket media-query-mediabucket-fb8oddjbslv1 to function media-query-dev-handle_object_removed
    Creating IAM role: media-query-dev-api_handler
    Creating lambda function: media-query-dev
    Creating Rest API
    Resources deployed:
      - Lambda ARN: arn:aws:lambda:us-west-2:123456789123:function:media-query-dev-handle_object_created
      - Lambda ARN: arn:aws:lambda:us-west-2:123456789123:function:media-query-dev-handle_object_removed
      - Lambda ARN: arn:aws:lambda:us-west-2:123456789123:function:media-query-dev
      - Rest API URL: https://1lmxgj9bfl.execute-api.us-west-2.amazonaws.com/api/


Verification
~~~~~~~~~~~~

1. Reupload the ``othersample.jpg`` image using the CLI::

    $ aws s3 cp ../chalice-workshop/code/media-query/final/assets/othersample.jpg s3://$MEDIA_BUCKET_NAME


2. Use HTTPie to query the deployed API for all media items::

    $ http $(chalice url)
    HTTP/1.1 200 OK
    Connection: keep-alive
    Content-Length: 126
    Content-Type: application/json
    Date: Tue, 17 Jul 2018 14:14:27 GMT
    Via: 1.1 a3c7cc30af6c8465e695a3c0d44793e0.cloudfront.net (CloudFront)
    X-Amz-Cf-Id: PAkgH2j5G2er_TZwyQOcwGahwNTR8dhEhrCUklcdDuuEBcKOYQ1-Ug==
    X-Amzn-Trace-Id: Root=1-5b4df9c1-89a47758a7a7989e47799a12;Sampled=0
    X-Cache: Miss from cloudfront
    x-amz-apigw-id: KLP2SFnTPHcFeqw=
    x-amzn-RequestId: b5e7488a-89cb-11e8-acbf-eda14961f501

    [
        {
            "labels": [
                "Human",
                "People",
                "Person",
                "Phone Booth",
                "Bus",
                "Transportation",
                "Vehicle",
                "Man",
                "Face",
                "Leisure Activities",
                "Tourist",
                "Portrait",
                "Crowd"
            ],
            "name": "othersample.jpg",
            "type": "image"
        },
        {
            "labels": [
                "Animal",
                "Canine",
                "Dog",
                "German Shepherd",
                "Mammal",
                "Pet",
                "Collie"
            ],
            "name": "sample.jpg",
            "type": "image"
        }
    ]


   Note ``chalice url`` just returns the URL of the remotely deployed API.


3. Use HTTPie to test out a couple of the query string parameters::

    $ http $(chalice url) label=='Phone Booth'
    HTTP/1.1 200 OK
    Connection: keep-alive
    Content-Length: 207
    Content-Type: application/json
    Date: Sun, 22 Jul 2018 07:49:37 GMT
    Via: 1.1 75fd15ce5d9f38e4c444039a1548df96.cloudfront.net (CloudFront)
    X-Amz-Cf-Id: nYpeS8kk_lFklCA7wCkOI0NO1wabDI3jvs3UpHFlsJ-c0nvlXNrvJQ==
    X-Amzn-Trace-Id: Root=1-5b543710-8beb4000395cd60e5688841a;Sampled=0
    X-Cache: Miss from cloudfront
    x-amz-apigw-id: Ka2KpF0nvHcF1hg=
    x-amzn-RequestId: c7e9cabf-8d83-11e8-b109-5f2c96dac9da

    [
        {
            "labels": [
                "Human",
                "People",
                "Person",
                "Phone Booth",
                "Bus",
                "Transportation",
                "Vehicle",
                "Man",
                "Face",
                "Leisure Activities",
                "Tourist",
                "Portrait",
                "Crowd"
            ],
            "name": "othersample.jpg",
            "type": "image"
        }
    ]

    $ http $(chalice url) startswith==sample
    HTTP/1.1 200 OK
    Connection: keep-alive
    Content-Length: 126
    Content-Type: application/json
    Date: Sun, 22 Jul 2018 07:51:03 GMT
    Via: 1.1 53657f22d99084ad547a21392858391b.cloudfront.net (CloudFront)
    X-Amz-Cf-Id: TORlA6wdOff5n4xHUH9ftnXNxFrTmQsSFG18acx7iwKLA_NsUoUoCg==
    X-Amzn-Trace-Id: Root=1-5b543766-912f6e067cb58ddcb6a973de;Sampled=0
    X-Cache: Miss from cloudfront
    x-amz-apigw-id: Ka2YEGNvPHcF8SA=
    x-amzn-RequestId: fb25c9e7-8d83-11e8-898d-8da83b49132b

    [
        {
            "labels": [
                "Animal",
                "Canine",
                "Dog",
                "German Shepherd",
                "Mammal",
                "Pet",
                "Collie"
            ],
            "name": "sample.jpg",
            "type": "image"
        }
    ]


4. Use HTTPie to query the deployed API for ``sample.jpg`` image::

    $ http $(chalice url)sample.jpg
    HTTP/1.1 200 OK
    Connection: keep-alive
    Content-Length: 124
    Content-Type: application/json
    Date: Tue, 17 Jul 2018 14:16:04 GMT
    Via: 1.1 7ca583dd6abc0b0f42b148142a75588a.cloudfront.net (CloudFront)
    X-Amz-Cf-Id: pzkZ0uZvk5e5W-ZV39v2zCCFAmmRJjDMJZ_I9GyDKhg6WEHotrMmnQ==
    X-Amzn-Trace-Id: Root=1-5b4dfa24-69d586d8e94fb75019b42f24;Sampled=0
    X-Cache: Miss from cloudfront
    x-amz-apigw-id: KLQFrF3svHcF32Q=
    x-amzn-RequestId: f0a6a6af-89cb-11e8-8420-e7ec8398ed6b

    {
        "labels": [
            "Animal",
            "Canine",
            "Dog",
            "German Shepherd",
            "Mammal",
            "Pet",
            "Collie"
        ],
        "name": "sample.jpg",
        "type": "image"
    }

