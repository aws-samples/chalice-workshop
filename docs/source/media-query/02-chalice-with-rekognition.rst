Part 2: Build a Chalice application using Rekognition
=====================================================

For this part of the tutorial, we will begin writing the media query Chalice
application and integrate Rekognition into the application. This initial
version of the application will accept the S3 bucket and key name of an image,
call the ``DetectLabels`` API on that stored image, and return the labels
detected for that image. So assuming the ``sample.jpg`` image is stored in a
bucket ``some-bucket`` under the key ``sample.jpg``, we will be able to invoke
the Lambda function to return the labels that Rekognition detected::

    $ chalice invoke --name detect_labels_on_image \
        --payload '{"Bucket": "some-bucket", "Key": "sample.jpg"}'
    ["Animal", "Canine", "Dog", "German Shepherd", "Mammal", "Pet", "Collie"]


For this section, we will be doing the following to create this version of the
application:

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
Create the new Chalice project for the Media Query application.

Instructions
~~~~~~~~~~~~

1. Create a new Chalice project called ``media-query`` with the ``new-project``
   command::

       $ chalice new-project media-query


Verification
~~~~~~~~~~~~

To ensure that the project was created, list the contents of the newly created
``mytodo`` directory::

    $ ls media-query
    app.py           requirements.txt


It should contain an ``app.py`` file and a ``requirements.txt`` file.


Copy over boilerplate files
---------------------------

Copy over starting files to facilitate development of the application

Instructions
~~~~~~~~~~~~

1. If you have not already done so, clone the repository for this workshop::

    $ git clone https://github.com/aws-samples/chalice-workshop.git


2. Copy over the ``chalicelib`` directory. This will contain utility modules
   for the application::

    $ cp -r chalice-workshop/code/media-query/02-chalice-with-rekognition/chalicelib media-query/


3. Copy over the ``.chalice/config.json`` and the ``.chalice/policy-dev.json``.
   The ``.chalice/config.json`` manages configuration of the Chalice
   application, and ``.chalice/policy-dev.json`` manages AWS permissions for
   the Chalice application::

   $ cp chalice-workshop/code/media-query/02-chalice-with-rekognition/.chalice/config.json media-query/.chalice
   $ cp chalice-workshop/code/media-query/02-chalice-with-rekognition/.chalice/policy-dev.json media-query/.chalice


4. Copy over the ``resources.json`` file and ``recordresources.py``. These two
   files will be used to deploy and integrate AWS resources into the
   Chalice application::

    $ cp chalice-workshop/code/media-query/02-chalice-with-rekognition/resources.json media-query/
    $ cp chalice-workshop/code/media-query/02-chalice-with-rekognition/recordresources.py media-query/


Verification
~~~~~~~~~~~~

1. Ensure the structure of the ``media-query`` directory is the
   following::

    $ tree -a media-query
    ├── .chalice
    │   ├── config.json
    │   └── policy-dev.json
    ├── .gitignore
    ├── app.py
    ├── chalicelib
    │   ├── __init__.py
    │   └── rekognition.py
    ├── recordresources.py
    ├── requirements.txt
    └── resources.json


Write a Lambda function for detecting labels
--------------------------------------------

Fill out the ``app.py`` file to write a Lambda function that detects labels
on an image stored in a S3 bucket.

Instructions
~~~~~~~~~~~~

1. Move into the ``media-query`` directory::

    $ cd media-query


2. Add ``boto3``, the AWS SDK for Python, as a dependency to the application
   in the ``requirements.txt``:

.. literalinclude:: ../../../code/media-query/03-add-db/requirements.txt
   :linenos:


3. Open the ``app.py`` file and delete all lines of code underneath
   the line: ``app = Chalice(app_name='media-query')``. Your ``app.py`` file
   should only consist of the following lines::

    from chalice import Chalice

    app = Chalice(app_name='media-query')


4. Import ``boto3`` and the ``chalicelib.rekognition`` module in your
   ``app.py`` file:

.. literalinclude:: ../../../code/media-query/03-add-db/app.py
   :linenos:
   :lines: 1-3
   :emphasize-lines: 1,3

4. Add a helper function for instantiating a Rekognition client:

.. literalinclude:: ../../../code/media-query/03-add-db/app.py
   :linenos:
   :lines: 1-15
   :emphasize-lines: 7,10-15

5. Add a new function ``detect_labels_on_image`` decorated by the
   ``app.lambda_function`` decorator that uses a rekognition client to detect
   labels on an image stored in a S3 bucket:

.. literalinclude:: ../../../code/media-query/03-add-db/app.py
   :linenos:
   :emphasize-lines: 18-22


Verification
~~~~~~~~~~~~

1. Ensure the contents of the ``requirements.txt`` file is:

.. literalinclude:: ../../../code/media-query/03-add-db/requirements.txt
   :linenos:

1. Ensure the contents of the ``app.py`` file is:

.. literalinclude:: ../../../code/media-query/03-add-db/app.py
   :linenos:


Create a S3 bucket
------------------

Create a S3 bucket to upload images and use with the Chalice application.

Instructions
~~~~~~~~~~~~

1. Use the AWS CLI and the ``resources.json`` CloudFormation template to deploy
   a CloudFormation stack ``media-query`` that contains a S3 bucket::

    $ aws cloudformation deploy --template-file resources.json \
        --stack-name media-query --capabilities CAPABILITY_IAM


Verification
~~~~~~~~~~~~

1. Retrieve and store the name of the S3 bucket using the AWS CLI::

    $ MEDIA_BUCKET_NAME=$(aws cloudformation describe-stacks --stack-name media-query --query "Stacks[0].Outputs[?OutputKey=='MediaBucketName'].OutputValue" --output text)


2. Ensure you can access the S3 bucket by listing its contents::

    $ aws s3 ls $MEDIA_BUCKET_NAME


   Note that the bucket should be empty.

Deploy the Chalice application
------------------------------

Deploy the chalice application.

Instructions
~~~~~~~~~~~~

1. Install the dependencies of the Chalice application::

    $ pip install -r requirements.txt


2. Run ``chalice deploy`` to deploy the application::

    $ chalice deploy
    Creating deployment package.
    Creating IAM role: media-query-dev-detect_labels_on_image
    Creating lambda function: media-query-dev-detect_labels_on_image
    Resources deployed:
      - Lambda ARN: arn:aws:lambda:us-west-2:123456789123:function:media-query-dev-detect_labels_on_image

Verification
~~~~~~~~~~~~

1. Upload the sample workshop image to the S3 bucket::

    $ aws s3 cp ../chalice-workshop/code/media-query/final/assets/sample.jpg s3://$MEDIA_BUCKET_NAME


2. Run ``chalice invoke`` on the ``detect_labels_on_image`` Lambda function::

    $ chalice invoke --name detect_labels_on_image \
        --payload "{\"Bucket\": \"$MEDIA_BUCKET_NAME\", \"Key\": \"sample.jpg\"}"


   It should return the following labels in the output::

    ["Animal", "Canine", "Dog", "German Shepherd", "Mammal", "Pet", "Collie"]
