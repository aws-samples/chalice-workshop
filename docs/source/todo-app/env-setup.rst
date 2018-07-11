Prerequisite: Setting up your environment
=========================================

To start working with AWS Chalice, there are two initial requirements your
development enviorment must have:

* Python 2.7
* Virtualenv
* AWS credentials
* git

If you have all of the above requirements, you can skip this step entirely.

Setting up Python
-----------------

This workshop will be using Python 2.7 for developing and running your Chalice
application.

First, check to see if Python 2.7 is already installed on your
development environment::

    $ python --version
    Python 2.7.12


It is important to note that for this workshop, the version does not
necessarily need to be ``2.7.12``. The patch version can be any value as long
as the major and minor version is ``2.7`` (e.g. ``2.7.10``, ``2.7.14``, etc.).
If the output has a major version of ``3``, you may have Python 2.7 installed
but default to Python 3::

    $ python --version
    Python 3.6.1


For this case, you can check if you have Python 2.7 installed by running::

    $ python2 --version
    Python 2.7.12


If your environment does have Python 2.7 installed, skip to the
`Setting up Virtualenv`_ step.


Installing Python 2.7 will vary base on operating systems.

OS X
~~~~

To install on OS X, make sure that ``brew`` is installed on your development
environment::

    $ brew --version


If ``brew`` is not installed (i.e. an error is thrown), then run the following
command to install ``brew``::

    $ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"


With ``brew`` now installed, run to install Python 2.7::

   $ brew install python


Once this command completes, check that Python now works on your machine by
checking the Python version::

    $ $(brew --prefix)/bin/python2 --version
    Python 2.7.12


If a Python 2.7 version is returned, then you have successfully installed
the required version of Python for this workshop.


Windows
~~~~~~~

To learn how to install Python 2.7 on Windows, follow instructions from
`The Hitchhiker's Guide to Python <http://docs.python-guide.org/en/latest/starting/install/win/>`__


Linux
~~~~~

To learn how to install Python 2.7 on Linux, follow instructions from
`The Hitchhiker's Guide to Python <http://docs.python-guide.org/en/latest/starting/install/linux/>`__


Setting up Virtualenv
---------------------

With Python 2.7 installed, it is important that ``virtualenv`` is also
installed. To see if ``virtualenv`` is already installed, run::

    $ virtualenv --version


This command should print out the version of ``virtualenv`` installed. If it
does print out the version, you have ``virtualenv`` already installed and
can skip the rest of this step.


If it does not, you will need to install ``virtualenv``. To install
``virtualenv``, first check to see if ``pip`` is installed in your development
environment::

    $ pip --version


If the command returns the ``pip`` version, you have ``pip`` already installed
in your development environment.

If this fails to run and you installed Python 2.7 with ``brew``, you still may
have it installed. Run the following to check::

    $(brew --prefix)/bin/pip2 --version


If you do not have ``pip`` installed, install ``pip`` by following the
instruction located in its
`documentation <https://pip.pypa.io/en/latest/installing/#installation>`__

Using ``pip``, now install ``virtualenv``::

    $ pip install virtualenv


Or the following if it was installed with ``brew``::

    $ (brew --prefix)/bin/pip2 install virtualenv


After installation completest, running the following command::

    $ virtualenv --version


Should now print out the version of ``virtualenv`` that got installed.


.. _aws-cli-setup:

Setting up AWS credentials
--------------------------

To use AWS Chalice, you will need AWS credentials. If you currently use one
of the AWS SDKs or the AWS CLI on your development environment, you should
already have AWS credentials set up and may skip this step. An easy way to
check this is by checking that you have either a ``~/.aws/credentials`` or
``~/.aws/config`` file on your machine.

First if you do not have AWS account, create one on the
`sign up page <https://portal.aws.amazon.com/billing/signup#/start>`__.

To actually set up AWS credentials on your development environment, use the
AWS CLI. To check if you have the AWS CLI installed, run::

    $ aws --version
    aws-cli/1.11.126 Python/2.7.10 Darwin/15.6.0 botocore/1.7.30


If it prints out a version such as ``aws-cli/1.11.126 Python/2.7.10 Darwin/15.6.0 botocore/1.7.30``, that means you have the AWS CLI installed on your
developement environment.

If you do not have the AWS CLI installed, you can install it by following the
instructions in the `user guide <http://docs.aws.amazon.com/cli/latest/userguide/installing.html>`__. Assuming ``pip`` is installed on your development
environment, the AWS CLI can be installed by running::

     $ pip install awscli


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
`instructions <http://docs.aws.amazon.com/general/latest/gr/managing-aws-access-keys.html>`__ for creating these keys. For the AWS region, it is recommend to
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
