Section 1: ``chalice package`` command
======================================

In this section, we'll use the ``chalice package`` command
to learn about the AWS CloudFormation integration with AWS chalice.


Initial Setup
-------------

We'll take our existing Todo app and create a SAM template.


Instructions
~~~~~~~~~~~~

The starting code for this step is in
``code/todo-app/part2/01-package-cmd``.  You can reuse your existing
sample application from part1 of this workshop.  If necessary,
you can copy over these files as a starting point for this
section::

    $ cp ../chalice-workshop/code/todo-app/part2/01-package-cmd/*.py .
    $ cp ../chalice-workshop/code/todo-app/part2/01-package-cmd/chalicelib/*.py chalicelib/
    $ cp ../chalice-workshop/code/todo-app/part2/01-package-cmd/.chalice/policy-dev.json .chalice/policy-dev.json

Now we're going to deploy our app using a CloudFormation stack.


1. First, ensure you have the AWS CLI installed. ::

    $ aws --version
    aws-cli/1.11.171 Python/2.7.14 Darwin/16.7.0 botocore/1.7.29

  If the AWS CLI is not installed, you can follow the instructions
  in the :ref:`aws-cli-setup` section.


Create a SAM template
---------------------

In this step, we're going to create a SAM template
using the ``chalice package`` command.

Instructions
~~~~~~~~~~~~

1. Create a SAM template for your app by using the ``chalice package``
   command::

    $ chalice package packaged/


Verification
~~~~~~~~~~~~

You should see two files in the ``packaged/`` directory, a
deployment zip file as well as a SAM template.


1. Verify the contents of the ``packaged/`` directory::

    $ ls -la packaged/
    .
    ..
    deployment.zip
    sam.json

2. Verify the contents of the ``deployment.zip``.  You should
   see your app.py file along with all the python library
   dependencies needed to run your app.  Chalice automatically
   handles managing dependencies based on your ``requirements.txt``
   file::

    $ unzip -l packaged/deployment.zip
    Archive:  packaged/deployment.zip
      Length      Date    Time    Name
    ---------  ---------- -----   ----
        31920  10-11-2017 16:28   chalice/app.py
          431  10-10-2017 11:40   chalice/__init__.py
          237  10-24-2017 11:30   app.py
                ...
         1159  10-24-2017 10:17   chalicelib/auth.py
         3647  10-24-2017 10:17   chalicelib/db.py
    ---------                     -------

3. Verify the contents of the ``sam.json`` file.  You don't have to
   understand the specifics of this file, but you'll notice that
   there's a few serverless resources defined::

    $ grep -B 1 'Serverless::' packaged/sam.json
        "RestAPI": {
          "Type": "AWS::Serverless::Api",
    --
        "APIHandler": {
          "Type": "AWS::Serverless::Function",


Deploy your SAM template
------------------------

Instructions
~~~~~~~~~~~~

Next, we'll use the AWS CLI to deploy our application through
AWS CloudFormation.

1. ``cd`` to the ``packaged`` directory::

    $ cd packaged/
    $ ls -la
    .
    ..
    deployment.zip
    sam.json

2. Next you'll need to create an Amazon S3 bucket.  When deploying
   your application with CloudFormation, your code is uploaded to
   an S3 bucket.  We can use the AWS CLI to create an S3 bucket.
   Keep in mind that S3 buckets are globally unique, so you'll need
   to use your own bucket name::

    $ aws s3 mb s3://chalice-workshop-cfn-bucket/ --region us-west-2

3. Use the AWS CLI to package your code.  This will upload your
   code to the S3 bucket you've created and create a new SAM
   template that references your S3 object. Make sure to use the
   same bucket you used in the previous step for the value of
   the ``--s3-bucket`` option::

     $ aws cloudformation package --template-file ./sam.json \
         --s3-bucket chalice-workshop-cfn-bucket \
         --output-template-file sam-packaged.yaml

4. Deploy your application using the AWS CLI. ::

    $ aws cloudformation deploy --template-file ./sam-packaged.yaml \
        --stack-name chalice-beta-stack \
        --capabilities CAPABILITY_IAM

   This command will take a few minutes to execute.  When this command
   finishes, you're chalice app will be up and running.



Verification
~~~~~~~~~~~~

1. Verify that the stack creation was successful::

    $ aws cloudformation describe-stacks --stack-name chalice-beta-stack \
        --query 'Stacks[0].StackStatus'
    "CREATE_COMPLETE"

2. Query the stack outputs to retrieve the endpoint URL of your
   REST API::

    $ aws cloudformation describe-stacks --stack-name chalice-beta-stack \
        --query 'Stacks[0].Outputs'
    [
        {
            "OutputKey": "APIHandlerArn",
            "OutputValue": "arn:aws:lambda:us-west-2:123:function:..."
        },
        {
            "OutputKey": "APIHandlerName",
            "OutputValue": "..."
        },
        {
            "OutputKey": "RestAPIId",
            "OutputValue": "abcd"
        },
        {
            "OutputKey": "EndpointURL",
            "OutputValue": "https://your-chalice-url/api/"
        }
    ]

3. Use the value for ``EndpointURL`` to test your API by creating
   a new Todo item::

    $ echo '{"description": "My third Todo", "metadata": {}}' | \
        http POST https://your-chalice-url/api/todos
    HTTP/1.1 200 OK
    Content-Length: 36
    Content-Type: application/json

    abcdefg-abcdefg

4. Verify you can retrieve this item::

    $ http https://your-chalice-url/todos/abcdefg-abcdefg
    HTTP/1.1 200 OK
    Content-Length: 140
    Content-Type: application/json

    {
        "description": "My third Todo",
        "metadata": {},
        "state": "unstarted",
        "uid": "abcdefg-abcdefg",
        "username": "default"
    }

Update your app
---------------

Now we'll make a change and deploy our change.


Instructions
~~~~~~~~~~~~

1. At the bottom of the ``app.py`` file, add a test route:


    .. code-block:: python

        @app.route('/test-route', methods=['GET'])
        def test_route():
            return {'test': 'route'}

2. Now we're going to use chalice and the AWS CLI to deploy
   this change.  Make sure you're at the top level directory
   of your app (the app.py should be in your current working
   directory).  Run the ``chalice package`` command::

    $ ls -la
    ...
    app.py
    $ chalice package packaged/

3. Run the ``aws cloudformation package`` command.  This will
   re-upload your code to S3.  Be sure to use the same
   bucket name you used in the previous step::

     $ cd packaged/
     $ aws cloudformation package --template-file ./sam.json \
         --s3-bucket chalice-workshop-cfn-bucket \
         --output-template-file sam-packaged.yaml

4. Deploy your application using the AWS CLI::

    $ aws cloudformation deploy --template-file ./sam-packaged.yaml \
        --stack-name chalice-beta-stack \
        --capabilities CAPABILITY_IAM

Verification
~~~~~~~~~~~~

1. Verify that the stack update was successful::

    $ aws cloudformation describe-stacks --stack-name chalice-beta-stack \
        --query 'Stacks[0].StackStatus'

2. Verify the new test route is available.  Use the same
   ``EndpointURL`` from the previous step::

    $ http https://your-chalice-url/api/test-route
    HTTP/1.1 200 OK
    Content-Length: 140
    Content-Type: application/json

    {"test": "route"}


Delete your stack
-----------------

We no longer need this CloudFormation stack.  In the next
section we'll use AWS CodePipeline to manage this CloudFormation
stack, so we can delete our existing stack.  Rather that
use ``chalice delete``, we're going to use the AWS CLI to delete
the CloudFormation stack we've created.

Instructions
~~~~~~~~~~~~

1. Delete your CloudFormation stack::

    $ aws cloudformation delete-stack --stack-name chalice-beta-stack

2. Wait for the deletion to successfully complete::

    $ aws cloudformation wait stack-delete-complete \
        --stack-name chalice-beta-stack

3. Delete the S3 bucket you've created.  Be sure to use the
   same bucket name you used when you created the bucket::

    $ aws s3 rb --force s3://chalice-workshop-cfn-bucket/ \
        --region us-west-2


Verification
~~~~~~~~~~~~

1. Verify the stack status::

    $ aws cloudformation describe-stacks --stack-name chalice-beta-stack \
        --query 'Stacks[0].StackStatus'

2. Verify the ``EndpointURL`` is no longer accessible::

    $ http https://your-chalice-url/api/test-route

    http: error: SSLError: [SSL: SSLV3_ALERT_HANDSHAKE_FAILURE] sslv3 alert
    handshake failure (_ssl.c:590) while doing GET request to URL:
    https://your-chalice-url/api/test-route

