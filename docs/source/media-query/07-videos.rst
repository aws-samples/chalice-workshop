Part 7: Add workflow to process videos
======================================

In the final part of this tutorial, we will add the ability to automatically
process videos uploaded to our S3 bucket and add them to our DynamoDB table.

To accomplish this we will be performing the following steps:

.. contents::
   :local:
   :depth: 1


Introduction to Rekognition object detection in videos
------------------------------------------------------

Detecting labels in a video is a different workflow than detecting image labels
when using Rekognition. Specifically, the workflow is asynchronous where you
must initiate a label detection job using the
`StartLabelDetection <https://docs.aws.amazon.com/rekognition/latest/dg/API_StartLabelDetection.html>`__
API and then call `GetLabelDetection <https://docs.aws.amazon.com/rekognition/latest/dg/API_GetLabelDetection.html>`__
once the job is complete to retrieve all of the detected labels. This step will
introduce you to this workflow.

Instructions
~~~~~~~~~~~~

1. Upload a sample video to the S3 bucket::

    $ aws s3 cp ../chalice-workshop/code/media-query/final/assets/sample.mp4 s3://$MEDIA_BUCKET_NAME


2. Run the ``start-label-detection`` command with the AWS CLI to start a
   label detection job on the uploaded video::

    $ aws rekognition start-label-detection \
        --video S3Object="{Bucket=$MEDIA_BUCKET_NAME,Name=sample.mp4}"
    {
      "JobId": "677b0209126a8fb9c1edc04759d22436b081e13fde955a2cb802c3434ba61b6c"
    }


3. Run the ``get-label-detection`` command until the ``JobStatus`` field is
   equal to ``SUCCEEDED`` and retrieve the video labels::

    $ aws rekognition get-label-detection --job-id 677b0209126a8fb9c1edc04759d22436b081e13fde955a2cb802c3434ba61b6c


Verification
~~~~~~~~~~~~

1. Once the ``JobStatus`` field is equal to ``SUCCEEDED``, the output of the
   ``get-label-detection`` command should contain::

    {
        "JobStatus": "SUCCEEDED",
        "VideoMetadata": {
            "Codec": "h264",
            "DurationMillis": 10099,
            "Format": "QuickTime / MOV",
            "FrameRate": 29.707088470458984,
            "FrameHeight": 960,
            "FrameWidth": 540
        },
        "Labels": [
            {
                "Timestamp": 0,
                "Label": {
                    "Name": "Animal",
                    "Confidence": 66.68909454345703
                }
            },
            {
                "Timestamp": 0,
                "Label": {
                    "Name": "Dog",
                    "Confidence": 60.80849838256836
                }
            },
            {
                "Timestamp": 0,
                "Label": {
                    "Name": "Husky",
                    "Confidence": 51.586997985839844
                }
            },
            {
                "Timestamp": 168,
                "Label": {
                    "Name": "Animal",
                    "Confidence": 58.79970169067383
                }
            },
         ...[SHORTENED]...
     }



Create SNS topic and IAM role
-----------------------------

Rekognition ``StartDetectLabels`` also has the option to publish a message to
an SNS topic once the job has completed. This is a much more efficient solution
than constantly polling the ``GetLabelDetection`` API to wait for the labels to
be detected. In this step, we will create an IAM role and SNS topic that
Rekognition can use to publish this message.

Instructions
~~~~~~~~~~~~

1. Copy the updated version of the ``resources.json`` CloudFormation template
   containing an IAM role and SNS topic for Rekognition to publish to::

    $ cp ../chalice-workshop/code/media-query/07-videos/resources.json .


2. Deploy the new resources to your CloudFormation stack using the AWS CLI::

    $ aws cloudformation deploy --template-file resources.json \
        --stack-name media-query --capabilities CAPABILITY_IAM

3. Save the SNS topic and IAM role information as environment variables in the
   Chalice application by running the ``recordresources.py`` script::

    $ python recordresources.py --stack-name media-query


Verification
~~~~~~~~~~~~

1. Ensure the contents of the ``config.json`` contains the
   environment variables ``VIDEO_TOPIC_NAME``, ``VIDEO_ROLE_ARN``, and
   ``VIDEO_TOPIC_ARN``::

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
            "MEDIA_BUCKET_NAME": "media-query-mediabucket-fb8oddjbslv1",
            "VIDEO_TOPIC_NAME": "media-query-VideoTopic-KU38EEHIIUV1",
            "VIDEO_ROLE_ARN": "arn:aws:iam::123456789123:role/media-query-VideoRole-1GKK0CA30VCAD",
            "VIDEO_TOPIC_ARN": "arn:aws:sns:us-west-2:123456789123:media-query-VideoTopic-KU38EEHIIUV1"
          }
        }
      }
    }


Deploy a lambda function for retrieving processed video labels
--------------------------------------------------------------

With the new SNS topic, add a new Lambda function that is triggered on
SNS messages to that topic, calls the ``GetDetectionLabel`` API, and adds the
video with the labels into the database.

Instructions
~~~~~~~~~~~~

1. In the ``app.py`` file, define the function ``add_video_file()`` that
   uses the
   `app.on_sns_message <https://chalice.readthedocs.io/en/latest/api.html#Chalice.on_sns_message>`__
   decorator:

   .. literalinclude:: ../../../code/media-query/final/app.py
      :lines: 58-59

2. Import ``json`` at the top of the ``app.py`` file:

   .. literalinclude:: ../../../code/media-query/final/app.py
      :lines: 1


3. Update the ``add_video_file()`` function, to process the ``event`` argument
   of type `SNSEvent <https://chalice.readthedocs.io/en/latest/api.html#SNSEvent>`__
   by retrieving the job ID from the message, retrieving the processed labels
   from Rekognition, and adding the video to the database:

   .. literalinclude:: ../../../code/media-query/final/app.py
      :lines: 58-65

3. Run ``chalice deploy`` to deploy the new Lambda function::

    $ chalice deploy
    Creating deployment package.
    Updating policy for IAM role: media-query-dev-handle_object_created
    Updating lambda function: media-query-dev-handle_object_created
    Configuring S3 events in bucket media-query-mediabucket-fb8oddjbslv1 to function media-query-dev-handle_object_created
    Updating policy for IAM role: media-query-dev-handle_object_removed
    Updating lambda function: media-query-dev-handle_object_removed
    Configuring S3 events in bucket media-query-mediabucket-fb8oddjbslv1 to function media-query-dev-handle_object_removed
    Creating IAM role: media-query-dev-add_video_file
    Creating lambda function: media-query-dev-add_video_file
    Subscribing media-query-dev-add_video_file to SNS topic media-query-VideoTopic-KU38EEHIIUV1
    Updating policy for IAM role: media-query-dev-api_handler
    Updating lambda function: media-query-dev
    Updating rest API
    Resources deployed:
      - Lambda ARN: arn:aws:lambda:us-west-2:123456789123:function:media-query-dev-handle_object_created
      - Lambda ARN: arn:aws:lambda:us-west-2:123456789123:function:media-query-dev-handle_object_removed
      - Lambda ARN: arn:aws:lambda:us-west-2:123456789123:function:media-query-dev-add_video_file
      - Lambda ARN: arn:aws:lambda:us-west-2:123456789123:function:media-query-dev
      - Rest API URL: https://1lmxgj9bfl.execute-api.us-west-2.amazonaws.com/api/


Verification
~~~~~~~~~~~~

1. Retrieve the arn of the deployed SNS topic::

    $ VIDEO_TOPIC_ARN=$(aws cloudformation describe-stacks --stack-name media-query --query "Stacks[0].Outputs[?OutputKey=='VideoTopicArn'].OutputValue" --output text)


2. Retrieve the arn of the deployed IAM role::

    $ VIDEO_ROLE_ARN=$(aws cloudformation describe-stacks --stack-name media-query --query "Stacks[0].Outputs[?OutputKey=='VideoRoleArn'].OutputValue" --output text)



3. Run the ``start-label-detection`` command with the AWS CLI to start a
   label detection job on the uploaded video::

    $ aws rekognition start-label-detection \
        --video S3Object="{Bucket=$MEDIA_BUCKET_NAME,Name=sample.mp4}" \
        --notification-channel SNSTopicArn=$VIDEO_TOPIC_ARN,RoleArn=$VIDEO_ROLE_ARN


4. Wait roughly twenty seconds and then use HTTPie to query for the video against the
   application's API::

    $ http $(chalice url)sample.mp4
    HTTP/1.1 200 OK
    Connection: keep-alive
    Content-Length: 151
    Content-Type: application/json
    Date: Tue, 17 Jul 2018 21:42:12 GMT
    Via: 1.1 aa42484f82c16d99015c599631def20c.cloudfront.net (CloudFront)
    X-Amz-Cf-Id: GpqmQOwnKcaxb2sP2fi-KSs8LCu24Q6ekKV8Oyo6a0HZ7kcnSGMpnQ==
    X-Amzn-Trace-Id: Root=1-5b4e62b4-da9db3b1e4c95470cbc2b160;Sampled=0
    X-Cache: Miss from cloudfront
    x-amz-apigw-id: KMRcNHUQvHcFaDQ=
    x-amzn-RequestId: 43c1cb91-8a0a-11e8-af84-8901f225e7d3

    {
        "labels": [
            "Clothing",
            "Bird Nest",
            "Dog",
            "Human",
            "People",
            "Person",
            "Husky",
            "Animal",
            "Nest",
            "Footwear"
        ],
        "name": "sample.mp4",
        "type": "video"
    }

Automate video workflow on S3 uploads and downloads
---------------------------------------------------

Now let's update the application so we do not have to manually invoke the
``StartLabelDetection`` API and instead have the API be invoked in
Lambda whenever a video is uploaded to S3. We will also need to automatically
delete the video whenever the video is deleted from S3.

Instructions
~~~~~~~~~~~~

1. Add the list ``_SUPPORTED_VIDEO_EXTENSTIONS`` representing a list of
   supported video extensions:

   .. literalinclude:: ../../../code/media-query/final/app.py
      :lines: 18-22


2. Update the ``handle_object_created`` function to start a video label
   detection job for videos uploaded to the S3 bucket and have the completion
   notification be published to the SNS topic:

   .. literalinclude:: ../../../code/media-query/final/app.py
      :lines: 42-50,105-113
      :emphasize-lines: 6-7,10-11,14-18

3. Update the ``handle_object_removed`` function to delete items from the
   table that are videos as well:

   .. literalinclude:: ../../../code/media-query/final/app.py
      :lines: 51-55
      :emphasize-lines: 4

4. Run ``chalice deploy`` to deploy the updated Chalice application::

    $ chalice deploy
    Creating deployment package.
    Updating policy for IAM role: media-query-dev-handle_object_created
    Updating lambda function: media-query-dev-handle_object_created
    Configuring S3 events in bucket media-query-mediabucket-fb8oddjbslv1 to function media-query-dev-handle_object_created
    Updating policy for IAM role: media-query-dev-handle_object_removed
    Updating lambda function: media-query-dev-handle_object_removed
    Configuring S3 events in bucket media-query-mediabucket-fb8oddjbslv1 to function media-query-dev-handle_object_removed
    Creating IAM role: media-query-dev-add_video_file
    Creating lambda function: media-query-dev-add_video_file
    Subscribing media-query-dev-add_video_file to SNS topic media-query-VideoTopic-KU38EEHIIUV1
    Updating policy for IAM role: media-query-dev-api_handler
    Updating lambda function: media-query-dev
    Updating rest API
    Resources deployed:
      - Lambda ARN: arn:aws:lambda:us-west-2:123456789123:function:media-query-dev-handle_object_created
      - Lambda ARN: arn:aws:lambda:us-west-2:123456789123:function:media-query-dev-handle_object_removed
      - Lambda ARN: arn:aws:lambda:us-west-2:123456789123:function:media-query-dev-add_video_file
      - Lambda ARN: arn:aws:lambda:us-west-2:123456789123:function:media-query-dev
      - Rest API URL: https://1lmxgj9bfl.execute-api.us-west-2.amazonaws.com/api/



Verification
~~~~~~~~~~~~

1. Delete the previously uploaded ``sample.mp4`` from the S3 bucket::

    $ aws s3 rm s3://$MEDIA_BUCKET_NAME/sample.mp4


2. Ensure the ``sample.mp4`` video no longer is queryable from the
   application's API::

    $ http $(chalice url)sample.mp4
    HTTP/1.1 404 Not Found
    Connection: keep-alive
    Content-Length: 88
    Content-Type: application/json
    Date: Tue, 17 Jul 2018 22:06:57 GMT
    Via: 1.1 e93b65cf89966087a2d9723b4713fb37.cloudfront.net (CloudFront)
    X-Amz-Cf-Id: XD7Wr8-zY8cUAEvnSU_ojyvAadTiNatcJXuztSmBta3Kiluvuvf6ug==
    X-Amzn-Trace-Id: Root=1-5b4e6880-c6c366d38f1e906798146b4b;Sampled=0
    X-Cache: Error from cloudfront
    x-amz-apigw-id: KMVEAFEPPHcFieQ=
    x-amzn-RequestId: b7fba401-8a0d-11e8-a7e4-a9e75b4bb382

    {
        "Code": "NotFoundError",
        "Message": "NotFoundError: Media file (sample.mp4) not found"
    }

3. Reupload the ``sample.mp4`` to the S3 bucket::

    $ aws s3 cp ../chalice-workshop/code/media-query/final/assets/sample.mp4 s3://$MEDIA_BUCKET_NAME


4. After waiting roughly 20 seconds, ensure the ``sample.mp4`` video is
   queryable again from the application's API::

    $ http $(chalice url)sample.mp4
    HTTP/1.1 200 OK
    Connection: keep-alive
    Content-Length: 151
    Content-Type: application/json
    Date: Tue, 17 Jul 2018 21:42:12 GMT
    Via: 1.1 aa42484f82c16d99015c599631def20c.cloudfront.net (CloudFront)
    X-Amz-Cf-Id: GpqmQOwnKcaxb2sP2fi-KSs8LCu24Q6ekKV8Oyo6a0HZ7kcnSGMpnQ==
    X-Amzn-Trace-Id: Root=1-5b4e62b4-da9db3b1e4c95470cbc2b160;Sampled=0
    X-Cache: Miss from cloudfront
    x-amz-apigw-id: KMRcNHUQvHcFaDQ=
    x-amzn-RequestId: 43c1cb91-8a0a-11e8-af84-8901f225e7d3

    {
        "labels": [
            "Clothing",
            "Bird Nest",
            "Dog",
            "Human",
            "People",
            "Person",
            "Husky",
            "Animal",
            "Nest",
            "Footwear"
        ],
        "name": "sample.mp4",
        "type": "video"
    }


Final Code
----------
Congratulations! You have now completed this tutorial. Below is the final code
that you should have wrote in the ``app.py`` of your application:

.. literalinclude:: ../../../code/media-query/final/app.py
   :linenos:

For the complete final application, see the
`GitHub repository <https://github.com/aws-samples/chalice-workshop/tree/events-workshop/code/media-query/final>`__
