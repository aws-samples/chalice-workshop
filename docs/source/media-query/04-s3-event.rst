Part 4: Add S3 event source
===========================

So far, we have been manually invoking the Lambda function ourselves in order
to detect objects in the image and add the information to our database.
However, we can automate this workflow using Lambda event sources so that
the Lambda function is invoked every time an object is uploaded to the S3
bucket.

For this section, we will be doing the following:

.. contents::
   :local:
   :depth: 1


Add Lambda event source for S3 object creation event
----------------------------------------------------

Change the Lambda function to be invoked whenever an object is uploaded to
a S3 bucket via the
`on_s3_event decorator <https://chalice.readthedocs.io/en/latest/topics/events.html#s3-events>`__.

Instructions
~~~~~~~~~~~~

1. In the ``app.py`` file, change the ``detect_labels_on_image`` signature to
   be named ``handle_object_created`` that accepts a single ``event``
   parameter::

    def handle_object_created(event):


2. Update the decorator on ``handle_object_created`` to use the
   ``app.on_s3_event`` decorator instead and have the Lambda function be
   triggered whenever an object is created in the bucket specified by the
   environment variable ``MEDIA_BUCKET_NAME``::

    @app.on_s3_event(bucket=os.environ['MEDIA_BUCKET_NAME'],
                     events=['s3:ObjectCreated:*'])
    def handle_object_created(event):


3. Add the list ``_SUPPORTED_IMAGE_EXTENSTIONS`` representing a list of
   supported image extensions:

   .. literalinclude:: ../../../code/media-query/05-s3-delete-event/app.py
      :lines: 12-15


4. Update the ``handle_object_created`` function to use the new ``event``
   argument of type `S3Event <https://chalice.readthedocs.io/en/latest/api.html#S3Event>`__
   and only do object detection and database additions on specific image
   file extensions:

   .. literalinclude:: ../../../code/media-query/05-s3-delete-event/app.py
      :lines: 35-48
      :emphasize-lines: 3-6,8-9,12-14


Validation
~~~~~~~~~~

1. Ensure the contents of the ``app.py`` file is:

.. literalinclude:: ../../../code/media-query/05-s3-delete-event/app.py
   :linenos:

Redeploy the Chalice application
--------------------------------

Deploy the updated Chalice application.

Instructions
~~~~~~~~~~~~

1. Run ``chalice deploy``::

    $ chalice deploy
    Creating deployment package.
    Creating IAM role: media-query-dev-handle_object_created
    Creating lambda function: media-query-dev-handle_object_created
    Configuring S3 events in bucket media-query-mediabucket-fb8oddjbslv1 to function media-query-dev-handle_object_created
    Deleting function: arn:aws:lambda:us-west-2:123456789123:function:media-query-dev-detect_labels_on_image
    Deleting IAM role: media-query-dev-detect_labels_on_image
    Resources deployed:
      - Lambda ARN: arn:aws:lambda:us-west-2:123456789123:function:media-query-dev-handle_object_created


Validation
~~~~~~~~~~

1. Upload the ``sample.jpg`` image to the S3 bucket under a new key name
   ``sample2.jpg``::

    $ aws s3 cp ../chalice-workshop/code/media-query/final/assets/sample.jpg s3://$MEDIA_BUCKET_NAME/sample2.jpg

2. Use the ``get-item`` CLI command to ensure the ``sample2.jpg`` data
   was automatically populated in the DynamoDB table::

    $ aws dynamodb get-item --table-name $MEDIA_TABLE_NAME \
        --key '{"name": {"S": "sample2.jpg"}}'
    {
        "Item": {
            "name": {
                "S": "sample2.jpg"
            },
            "labels": {
                "L": [
                    {
                        "S": "Animal"
                    },
                    {
                        "S": "Canine"
                    },
                    {
                        "S": "Dog"
                    },
                    {
                        "S": "German Shepherd"
                    },
                    {
                        "S": "Mammal"
                    },
                    {
                        "S": "Pet"
                    },
                    {
                        "S": "Collie"
                    }
                ]
            },
            "type": {
                "S": "image"
            }
        }
    }

   If the item does not appear, try running the ``get-item`` command after
   waiting for ten seconds. Sometimes, it takes a little bit of time for the
   Lambda function to get triggered.
