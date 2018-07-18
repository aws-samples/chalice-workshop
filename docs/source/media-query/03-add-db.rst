Part 3: Integrate with a DynamoDB table
=======================================

Now that we have a Lambda function that can detect labels in an image, let's
integrate a DynamoDB table so we can query information across the various
images stored in our bucket. So instead of returning the labels, the Chalice
application will store the items in a DynamoDB table.

For this section, we will be doing the following to integrate the DynamoDB
table:

.. contents::
   :local:
   :depth: 1


Copy over boilerplate files
---------------------------

Copy over files needed for integrating the DynamoDB table into the application

Instructions
~~~~~~~~~~~~

1. Copy the ``db.py`` module into the ``chalicelib`` package::

    $ cp ../chalice-workshop/code/media-query/03-add-db/chalicelib/db.py chalicelib/


2. Copy over an updated version of the ``resources.json`` file::

    $ cp ../chalice-workshop/code/media-query/03-add-db/resources.json .


Verification
~~~~~~~~~~~~

1. Ensure the structure of the ``media-query`` directory includes the
   following files and directories::

    $ tree -a .
    ├── .chalice
    │   ├── config.json
    │   └── policy-dev.json
    ├── .gitignore
    ├── app.py
    ├── chalicelib
    │   ├── __init__.py
    │   ├── db.py
    │   └── rekognition.py
    ├── recordresources.py
    ├── requirements.txt
    └── resources.json

   Note there will be more files listed with ``tree`` assuming you already
   deployed the application once.

2. Ensure the contents of the ``resources.json`` is now the following::

    $ cat resources.json
    {
      "Outputs": {
        "MediaBucketName": {
          "Value": {
            "Ref": "MediaBucket"
          }
        },
        "MediaTableName": {
          "Value": {
            "Ref": "MediaTable"
          }
        }
      },
      "Resources": {
        "MediaBucket": {
          "Type": "AWS::S3::Bucket"
        },
        "MediaTable": {
          "Properties": {
            "AttributeDefinitions": [
              {
                "AttributeName": "name",
                "AttributeType": "S"
              }
            ],
            "KeySchema": [
              {
                "AttributeName": "name",
                "KeyType": "HASH"
              }
            ],
            "ProvisionedThroughput": {
              "ReadCapacityUnits": 5,
              "WriteCapacityUnits": 5
            }
          },
          "Type": "AWS::DynamoDB::Table"
        }
      }
    }


Create a DynamoDB table
-----------------------

Create a DynamoDB table to store and query information about images in the S3
bucket.

Instructions
~~~~~~~~~~~~

1. Use the AWS CLI and the ``resources.json`` CloudFormation template to
   redeploy the ``media-query`` CloudFormation stack to create a new
   DynamoDB ::

    $ aws cloudformation deploy --template-file resources.json \
        --stack-name media-query --capabilities CAPABILITY_IAM


Verification
~~~~~~~~~~~~

1. Retrieve and store the name of the DynamoDB table using the AWS CLI::

    $ MEDIA_TABLE_NAME=$(aws cloudformation describe-stacks --stack-name media-query --query "Stacks[0].Outputs[?OutputKey=='MediaTableName'].OutputValue" --output text)


2. Ensure the existence of the table using the ``describe-table`` CLI command::

    $ aws dynamodb describe-table --table-name $MEDIA_TABLE_NAME
    {
        "Table": {
            "AttributeDefinitions": [
                {
                    "AttributeName": "name",
                    "AttributeType": "S"
                }
            ],
            "TableName": "media-query-MediaTable-10QEPR0O8DOT4",
            "KeySchema": [
                {
                    "AttributeName": "name",
                    "KeyType": "HASH"
                }
            ],
            "TableStatus": "ACTIVE",
            "CreationDateTime": 1531769158.804,
            "ProvisionedThroughput": {
                "NumberOfDecreasesToday": 0,
                "ReadCapacityUnits": 5,
                "WriteCapacityUnits": 5
            },
            "TableSizeBytes": 0,
            "ItemCount": 0,
            "TableArn": "arn:aws:dynamodb:us-west-2:123456789123:table/media-query-MediaTable-10QEPR0O8DOT4",
            "TableId": "00eebe92-d59d-40a2-b5fa-32e16b571cdc"
        }
    }

Integrate the DynamoDB table
----------------------------

Integrate the newly created DynamoDB table into the Chalice application.

Instructions
~~~~~~~~~~~~

1. Save the DynamoDB table name as an environment variable in the Chalice
   application by running the ``recordresources.py`` script::

    $ python recordresources.py --stack-name media-query


2. Import ``os`` and the ``chalicelib.db`` module in your ``app.py`` file:

.. literalinclude:: ../../../code/media-query/04-s3-event/app.py
   :linenos:
   :lines: 1-6
   :emphasize-lines: 1,5

3. Add a helper function for instantiating a ``db.DynamoMediaDB`` class using
   the DynamoDB table name stored as an environment variable:

.. literalinclude:: ../../../code/media-query/04-s3-event/app.py
   :linenos:
   :lines: 1-20
   :emphasize-lines: 10,14-20

4. Update the ``detect_labels_on_image`` Lambda function to save the image
   along with the detected labels to the database:

.. literalinclude:: ../../../code/media-query/04-s3-event/app.py
   :linenos:
   :lines: 1-36
   :emphasize-lines: 35-36


Verification
~~~~~~~~~~~~

1. Ensure the contents of the ``config.json`` contains environment variables
   for ``MEDIA_TABLE_NAME``::

    $ cat .chalice/config.json
    {
      "version": "2.0",
      "app_name": "media-query",
      "stages": {
        "dev": {
          "api_gateway_stage": "api",
          "autogen_policy": false,
          "environment_variables": {
            "MEDIA_TABLE_NAME": "media-query-MediaTable-10QEPR0O8DOT4",
            "MEDIA_BUCKET_NAME": "media-query-mediabucket-fb8oddjbslv1"
          }
        }
      }
    }


   Note that the ``MEDIA_BUCKET_NAME`` will be present as well in the
   environment variables. It will be used in the next part of the tutorial.

2. Ensure the contents of the ``app.py`` file is:

.. literalinclude:: ../../../code/media-query/04-s3-event/app.py
   :linenos:

Redeploy the Chalice application
--------------------------------

Deploy the updated Chalice application.

Instructions
~~~~~~~~~~~~

1. Run ``chalice deploy``::

    $ chalice deploy
    Creating deployment package.
    Updating policy for IAM role: media-query-dev-detect_labels_on_image
    Updating lambda function: media-query-dev-detect_labels_on_image
    Resources deployed:
      - Lambda ARN: arn:aws:lambda:us-west-2:123456789123:function:media-query-dev-detect_labels_on_image

Verification
~~~~~~~~~~~~

1. Run ``chalice invoke`` with the ``sample-event.json`` on the updated
   ``detect_labels_on_image`` Lambda function::

    $ chalice invoke --name detect_labels_on_image < sample-event.json
    null

2. Use the ``get-item`` CLI command to ensure the ``sample.jpg`` data
   was populated in the DynamoDB table::

    $ aws dynamodb get-item --table-name $MEDIA_TABLE_NAME \
        --key '{"name": {"S": "sample.jpg"}}'
    {
        "Item": {
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
    }
