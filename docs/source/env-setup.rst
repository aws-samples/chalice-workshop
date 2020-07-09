Prerequisite: Setting up your environment
=========================================

To start working with AWS Chalice, there are some requirements your
development environment must have:

* Python 3.7
* Virtualenv
* AWS credentials
* git

If you have all of the above requirements, you can skip these steps entirely.

.. contents::
   :local:
   :depth: 1


Setting up Python
-----------------

This workshop requires Python 3.7 for developing and running your
Chalice application.

First, check to see if Python is already installed on your development
environment::

    $ python --version
    Python 3.7.3


It is important to note that for this workshop, the version does not
necessarily need to be ``3.7.3``. The patch version can be any value as long
as the major and minor version is ``3.7``.

Installing Python will vary base on operating systems.

OS X
~~~~

To install on OS X, make sure that ``brew`` is installed on your development
environment::

    $ brew --version


If ``brew`` is not installed (i.e. an error is thrown), then run the following
command to install ``brew``::

    $ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"


With ``brew`` now installed, run to install Python::

   $ brew install python


Once this command completes, check that Python now works on your machine by
checking the Python version::

    $ $(brew --prefix)/bin/python3 --version
    Python 3.7.3


If a Python 3.7 version is returned, then you have successfully installed
the required version of Python for this workshop.


Windows
~~~~~~~

To learn how to install Python on Windows, follow instructions from
`The Hitchhiker's Guide to Python <https://docs.python-guide.org/starting/install3/win/#install3-windows>`__


Linux
~~~~~

To learn how to install Python on Linux, follow instructions from
`The Hitchhiker's Guide to Python <https://docs.python-guide.org/starting/install3/linux/#install3-linux>`__


.. _aws-cli-setup:

Setting up AWS credentials
--------------------------

To use AWS Chalice, you will need AWS credentials. If you currently use one
of the AWS SDKs or the AWS CLI on your development environment, you should
already have AWS credentials set up and may skip this step. An easy way to
check this is by checking that you have either a ``~/.aws/credentials`` or
``~/.aws/config`` file on your machine.

First if you do not have AWS account, create one on the
`sign up page <https://portal.aws.amazon.com/billing/signup>`__.

To actually set up AWS credentials on your development environment, use the
AWS CLI. To check if you have the AWS CLI installed, run::

    $ aws --version
    aws-cli/1.15.60 Python/3.7.3 Darwin/15.6.0 botocore/1.10.59


If it prints out a version, that means you have the AWS CLI installed on your
development environment. To get credentials set, it should not matter what
version of the AWS CLI you are using. The tutorial you choose to follow will
inform you if you need a specific version of the AWS CLI.

If you do not have the AWS CLI v2 installed, you can install it by following the
instructions in the `user guide <https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html>`__.

With the AWS CLI installed, run ``aws configure`` to configure your
development environment for AWS credentials via its prompts::

    $ aws configure
    AWS Access Key ID [None]: ****************ABCD
    AWS Secret Access Key [None]: ****************abCd
    Default region name [None]: us-west-2
    Default output format [None]:


For the ``aws configure`` command you will only need to provide an AWS Access
Key ID, AWS Secret Access Key, and AWS region. To get an AWS Access Key and
Secret Access Key, follow the
`instructions <https://docs.aws.amazon.com/general/latest/gr/managing-aws-access-keys.html>`__ for creating these keys. For the AWS region, it is recommend to
set this to ``us-west-2``, but any region may be used.

Finally to check that everything is correctly set up, run the following AWS
CLI::

    $ aws ec2 describe-regions


This should return a JSON response back about all of the AWS regions supported
by Amazon EC2. This indicates that the AWS credentials have been properly
configured in your development environment.


.. _git-setup:

Setting up git
--------------

You will need to clone a git repository so you should make sure you have
have git installed on your development machine.

First, see if you already have git installed::

  $ git --version


If you do not have git installed you will have to follow the section below
for your system.

OS X
~~~~

To install on OS X, make sure that ``brew`` is installed on your development
environment::

    $ brew --version


If ``brew`` is not installed (i.e. an error is thrown), then run the following
command to install ``brew``::

    $ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"


With ``brew`` now installed, run to install git::

  $ brew install git

Linux
~~~~~

Depending on your distro, git should be available in your standard package
manager. Try one of the following commands::

  $ sudo apt-get install git

::

  $ sudo yum install git


Windows
~~~~~~~

For Windows, you will need to manually download and install a git
client such as `git-scm <https://git-scm.com/download/win/>`_.


Optional requirements
---------------------

Below is a set of tools that are not required to be installed but would
facilitate the workshop:

Tree
~~~~

A command line tool for recursively listing the structure of a directory. First
check to see if you have ``tree`` installed::

  $ tree --version


If it fails to return a version number, you should try to install it. To
install on OSX, run the following::

  $ brew install tree

For Linux, ``tree`` should be available in your standard package
manager. Try one of the following commands::

  $ sudo apt-get install tree

::

  $ sudo yum install tree
