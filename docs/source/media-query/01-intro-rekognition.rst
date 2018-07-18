Part 1: Introduction to Amazon Rekognition
==========================================

The application being built will leverage
`Amazon Rekognition <https://aws.amazon.com/rekognition/>`__ to detect objects
in images and videos. This part of the tutorial will teach you how more about
Rekognition and how to interact with its API.


Install the AWS CLI
-------------------

To interact with the Rekognition API, the AWS CLI will need to be installed.

Instructions
~~~~~~~~~~~~
1. Check to see the CLI is installed::

    $ aws --version
    aws-cli/1.15.60 Python/3.6.5 Darwin/15.6.0 botocore/1.10.59

   The version of the CLI must be version 1.15.60 or greater.

2a. If the CLI is not installed, follow the installation instructions in the
    :ref:`aws-cli-setup` section.

2b. If your current CLI version is older than the minimum required version,
    follow the upgrade instructions in the
    `user guide <https://docs.aws.amazon.com/cli/latest/userguide/installing.html>`__
    to upgrade to the latest version of the AWS CLI. If you installed the AWS
    CLI with ``pip``, you can run the following command to upgrade to the
    latest version::

    $ pip install awscli --upgrade


Verification
~~~~~~~~~~~~

1. Run the following command::

    $ aws --version
    aws-cli/1.15.60 Python/3.6.1 Darwin/15.6.0 botocore/1.10.59

   The version displayed of the CLI must be version 1.15.60 or greater.


Detect image labels using Rekognition
-------------------------------------

Use the Rekognition API via the AWS CLI to detect labels in an image.

Instructions
~~~~~~~~~~~~

1. If you have not already done so, clone the repository for this workshop::

    $ git clone https://github.com/aws-samples/chalice-workshop.git

2. Use the ``detect-labels`` command to detect labels on a sample image::

    $ aws rekognition detect-labels \
        --image-bytes fileb://chalice-workshop/code/media-query/final/assets/sample.jpg


Verification
~~~~~~~~~~~~

The output of the ``detect-labels`` command should be::

    {
        "Labels": [
            {
                "Confidence": 85.75711822509766,
                "Name": "Animal"
            },
            {
                "Confidence": 85.75711822509766,
                "Name": "Canine"
            },
            {
                "Confidence": 85.75711822509766,
                "Name": "Dog"
            },
            {
                "Confidence": 85.75711822509766,
                "Name": "German Shepherd"
            },
            {
                "Confidence": 85.75711822509766,
                "Name": "Mammal"
            },
            {
                "Confidence": 85.75711822509766,
                "Name": "Pet"
            },
            {
                "Confidence": 84.56783294677734,
                "Name": "Collie"
            }
        ]
    }
