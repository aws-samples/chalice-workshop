.. ChaliceWorkshop documentation master file, created by
   sphinx-quickstart on Mon Oct 16 12:51:22 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

AWS Chalice Workshop
====================

Welcome to the AWS Chalice Workshop! This site contains various tutorials
on how you can build serverless applications using AWS Chalice. To begin,
please make sure your environment is set up correctly by following the
`Environment Setup tutorial <env-setup.html>`__. Then select one of the
following tutorials to follow:

* `Todo Application <todo-app/index.html>`__: A serverless web application
  to manage Todo's. This tutorial will walk through creating a serverless
  web API to create, update, get, and delete Todo's, managing Todo's in
  a database, adding authorization with JWT, and creating a full CI/CD
  pipeline for the application. AWS services covered include AWS Lambda,
  Amazon API Gateway, Amazon DynamoDB, AWS CodeBuild, and AWS CodePipeline.

* `Media Query Application <media-query/index.html>`__: A serverless
  application for querying media files in an Amazon S3 bucket. This tutorial
  will walk through using AWS Lambda event sources to create an automated
  workflow that processes uploaded media files and stores the processed
  information in a database. It will also walk through how to create a web API
  to query the processed information in the database. AWS services covered
  include AWS Lambda, Amazon Rekognition, Amazon S3, Amazon DynamoDB,
  Amazon API Gateway, and Amazon SNS.


.. toctree::
   :hidden:
   :maxdepth: 3

   env-setup
   todo-app/index
   media-query/index
