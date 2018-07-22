Part 5: Add S3 delete event handler
===================================

Now that we are automatically importing uploaded images to our table, we need
to be able to automatically delete images from our table that get deleted
from our bucket. This can be accomplished by doing the following:

.. contents::
   :local:
   :depth: 1


Add Lambda function for S3 object deletion
------------------------------------------

Add a new Lambda function that is invoked whenever an object is deleted from
the S3 bucket and if it is an image, removes the image from the table.

Instructions
~~~~~~~~~~~~

1. In the ``app.py`` file add a new function ``handle_object_removed`` that
   is triggered whenever an object gets deleted from the bucket and
   deletes the item from table if it is an image:

  .. literalinclude:: ../../../code/media-query/06-web-api/app.py
     :lines: 42-46


Verification
~~~~~~~~~~~~

1. Ensure the contents of the ``app.py`` file is:

.. literalinclude:: ../../../code/media-query/06-web-api/app.py
   :linenos:


Redeploy the Chalice application
--------------------------------

Deploy the updated Chalice application with the new Lambda function.

Instructions
~~~~~~~~~~~~

1. Run ``chalice deploy``::

    $ chalice deploy
    Creating IAM role: media-query-dev-handle_object_removed
    Creating lambda function: media-query-dev-handle_object_removed
    Configuring S3 events in bucket media-query-mediabucket-fb8oddjbslv1 to function media-query-dev-handle_object_removed
    Resources deployed:
      - Lambda ARN: arn:aws:lambda:us-west-2:123456789123:function:media-query-dev-handle_object_created
      - Lambda ARN: arn:aws:lambda:us-west-2:123456789123:function:media-query-dev-handle_object_removed


Verification
~~~~~~~~~~~~

1. Delete the uploaded ``othersample.jpg`` object from the previous part::

    $ aws s3 rm s3://$MEDIA_BUCKET_NAME/othersample.jpg


2. Use the ``scan`` CLI command to ensure the object is no longer in the
   table::

    $ aws dynamodb scan --table-name $MEDIA_TABLE_NAME
    {
        "Items": [
            {
                "name": {
                    "S": "sample.jpg"
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
        ],
        "Count": 1,
        "ScannedCount": 1,
        "ConsumedCapacity": null
    }


   If the item still appears, try running the ``scan`` command after
   waiting for ten seconds. Sometimes, it takes a little bit of time for the
   Lambda function to get triggered. In the end, the table should only have the
   ``sample.jpg`` item.
