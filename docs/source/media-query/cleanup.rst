Cleaning up the Chalice application
===================================

This part of the tutorial provides instructions on how you can clean up your
deployed resources once you are done using this application. This set of
instructions can be completed at any point during the tutorial to clean up the
application.

Instructions
------------


1. Delete the chalice application::

    $ chalice delete
    Deleting Rest API: kyfn3gqcf0
    Deleting function: arn:aws:lambda:us-west-2:123456789123:function:media-query-dev
    Deleting IAM role: media-query-dev-api_handler
    Deleting function: arn:aws:lambda:us-west-2:123456789123:function:media-query-dev-add_video_file
    Deleting IAM role: media-query-dev-add_video_file
    Deleting function: arn:aws:lambda:us-west-2:123456789123:function:media-query-dev-handle_object_removed
    Deleting IAM role: media-query-dev-handle_object_removed
    Deleting function: arn:aws:lambda:us-west-2:123456789123:function:media-query-dev-handle_object_created
    Deleting IAM role: media-query-dev-handle_object_created

2. Delete all objects in your S3 bucket::

    $ aws s3 rm s3://$MEDIA_BUCKET_NAME --recursive
    delete: s3://media-query-mediabucket-4b1h8anboxpa/sample.jpg
    delete: s3://media-query-mediabucket-4b1h8anboxpa/sample.mp4

3. Delete the CloudFormation stack containing the additional AWS resources::

    $ aws cloudformation delete-stack --stack-name media-query

Validation
----------

1. Ensure that the API for the application no longer exists::

    $ chalice url
    Error: Could not find a record of a Rest API in chalice stage: 'dev'


2. Check the existence of a couple of resources from the CloudFormation stack
   to make sure the resources no longer exist::

    $ aws s3 ls s3://$MEDIA_BUCKET_NAME
    An error occurred (NoSuchBucket) when calling the ListObjects operation: The specified bucket does not exist

    $ aws dynamodb describe-table --table-name $MEDIA_TABLE_NAME
    An error occurred (ResourceNotFoundException) when calling the DescribeTable operation: Requested resource not found: Table: media-query-MediaTable-YIM7BMEIOF8Y not found
