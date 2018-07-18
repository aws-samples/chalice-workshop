Prerequisite: Setting up your environment
=========================================

To start working with AWS Chalice, there are two initial requirements your
development environment must have:

* Python 2.7 or 3.6
* Virtualenv
* AWS credentials
* git

If you have all of the above requirements, you can skip these steps entirely.

.. contents::
   :local:
   :depth: 1


Setting up Python
-----------------

This workshop requires Python 2.7 or 3.6 for developing and running your
Chalice application. It is your choice on which version of Python you want to
use for this workshop. However, Python 3.6 is recommended.

First, check to see if Python is already installed on your development
environment::

    $ python --version
    Python 3.6.5


It is important to note that for this workshop, the version does not
necessarily need to be ``3.6.5``. The patch version can be any value as long
as the major and minor version is ``3.6`` (or ``2.7`` if you elected to use
Python 2.7 instead).


If your environment does have Python 2.7 or 3.6 installed, skip to the
`Setting up Virtualenv`_ step.


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
    Python 3.6.5


If a Python 3.6 version is returned, then you have successfully installed
the required version of Python for this workshop.

.. note::

   If Python 3.7 was installed instead of Python 3.6, you can force Python 3.6
   by first removing the symlink::

     $ brew unlink python

   ``git checkout`` to the specific ``python`` formula where Python
   3.6 was the latest version::

     $ git checkout f2a764e /usr/local/Homebrew/Library/Taps/homebrew/homebrew-core/Formula/python.rb


   Then run ``brew install`` again::

     $ brew install python


   And Python 3.6 should now be installed::

     $ $(brew --prefix)/bin/python3 --version
     Python 3.6.5

Windows
~~~~~~~

To learn how to install Python on Windows, follow instructions from
`The Hitchhiker's Guide to Python <https://docs.python-guide.org/starting/install3/win/#install3-windows>`__


Linux
~~~~~

To learn how to install Python on Linux, follow instructions from
`The Hitchhiker's Guide to Python <https://docs.python-guide.org/starting/install3/linux/#install3-linux>`__


Setting up Virtualenv
---------------------

With Python 2.7 or 3.6 installed, it is important that ``virtualenv`` is also
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

If this fails to run and you installed Python with ``brew``, you still may
have it installed. Run the following to check::

    $ $(brew --prefix)/bin/pip3 --version


If you do not have ``pip`` installed, install ``pip`` by following the
instruction located in its
`documentation <https://pip.pypa.io/en/latest/installing/#installation>`__

Using ``pip``, now install ``virtualenv``::

    $ pip install virtualenv


Or the following if it was installed with ``brew``::

    $ (brew --prefix)/bin/pip3 install virtualenv


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
`sign up page <https://portal.aws.amazon.com/billing/signup>`__.

To actually set up AWS credentials on your development environment, use the
AWS CLI. To check if you have the AWS CLI installed, run::

    $ aws --version
    aws-cli/1.15.60 Python/3.6.5 Darwin/15.6.0 botocore/1.10.59


If it prints out a version, that means you have the AWS CLI installed on your
development environment. To get credentials set, it should not matter what
version of the AWS CLI you are using. The tutorial you choose to follow will
inform you if you need a specific version of the AWS CLI.

If you do not have the AWS CLI installed, you can install it by following the
instructions in the `user guide <https://docs.aws.amazon.com/cli/latest/userguide/installing.html>`__. Assuming ``pip`` is installed on your development
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
