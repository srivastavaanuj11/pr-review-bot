PR Review Bot
=============

|python| |MIT| |black|

.. |python| image:: https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue?logo=python&logoColor=white
   :target: https://github.com/srivastavaanuj11/pr-review-bot/blob/main/pyproject.toml
   :alt: Python

.. |MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: MIT

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=flat
   :target: https://github.com/psf/black
   :alt: Black

Overview
--------

The ``pr-review-bot`` package is a Python development tool for leveraging
the power of OpenAI to automatically generate suggestions for improving
GitHub pull requests and local changes. To generate suggestions for improvements,
this tool considers code style, logical errors, and other possible issues. Using
this tool makes the code review process smoother and more efficient,
ensuring that your code base is high quality, easy to maintain, and
adheres to best practices.


Installation
------------

The ``pr-review-bot`` package requires Python 3.10 or later. It is not published on
PyPI: the ``pr-review-bot`` project on PyPI is a different, unrelated package. Install
this package from its GitHub repository instead.

Two installation modes are provided: user and developer.

For users
^^^^^^^^^

First, to make sure that you have the latest version of `pip`_,
run this command:

.. code:: bash

    python -m pip install -U pip

Then, to install the ``pr-review-bot`` package, run this command:

.. code:: bash

    python -m pip install git+https://github.com/srivastavaanuj11/pr-review-bot.git

For developers
^^^^^^^^^^^^^^

To install the package in editable mode with its test dependencies, clone the
repository and install it from the repository root with these commands:

.. code:: bash

    git clone https://github.com/srivastavaanuj11/pr-review-bot.git
    cd pr-review-bot
    python -m pip install -U pip
    python -m pip install -e ".[tests]"

To run the tests with `pytest`_, run this command:

.. code:: bash

    pytest

Most tests call the GitHub and OpenAI APIs, so they need the tokens and environment
variables described in `Token configuration`_.

To build the documentation with `Sphinx`_, run these commands:

.. code:: bash

    python -m pip install -e ".[doc]"
    make -C doc html

The code style is checked with `black`_ and `isort`_, configured in ``pyproject.toml``,
and `flake8`_, configured in ``.flake8``. To check your changes, run these commands:

.. code:: bash

    python -m pip install black isort flake8
    black --check src tests doc
    isort --check-only src tests doc
    flake8 src tests doc


Token configuration
-------------------

To use this tool to review GitHub pull requests, you must have two tokens for
accessing the bot functionalities:

- GitHub access token
- Azure OpenAI token

Reviewing a local repository with the `CLI <CLI usage_>`__ requires only the OpenAI token
and settings.

Subsequent sections explain how to obtain these tokens and set them up for your project.

Ensure that you keep your tokens confidential and do not share them publicly. Additionally,
always follow the best security practices to protect your project and data from unauthorized
access.


GitHub access token
^^^^^^^^^^^^^^^^^^^

A GitHub access token is required to access the GitHub API for certain features, such as
querying repositories, creating issues, and managing pull requests.

To obtain a GitHub access token, perform these steps:

1. **Create a GitHub account:** If you do not already have a GitHub account, sign up for one
   at https://github.com/signup.

2. **Generate a PAT (personal access token):** After signing into your GitHub account, go to
   `Personal access tokens (classic) <https://github.com/settings/tokens>`_ in your GitHub
   developer settings and click **Generate new token**, then **Generate new token (classic)**.
   Follow the prompts to configure your new token, choosing the scope of access required
   based on your project's needs.

3. **Copy the token:** After creating the token, GitHub displays it only once. Make sure
   that you copy the token to a secure location because you are not able to see it again.

4. **Set the token as an environment variable:** To use the project with your GitHub access
   token, set the token as an environment variable having this name: ``GITHUB_TOKEN``.

Azure OpenAI token
^^^^^^^^^^^^^^^^^^

The Azure OpenAI token is required to access the OpenAI API for utilizing the advanced AI
capabilities provided by `Microsoft Azure <https://portal.azure.com/>`_.

To obtain an Azure OpenAI token, perform these steps:

1. **Sign up for Azure:** If you do not already have an Azure account, sign up for a free
   account at https://azure.com/free.

2. **Create an Azure OpenAI resource:** Once you have an Azure account, create an Azure
   OpenAI resource in the Azure portal and deploy a chat model in it. This resource provides
   you with the necessary credentials to access the OpenAI API.

3. **Copy the token:** After creating the resource, open its **Keys and Endpoint** page and
   copy one of the keys. This key is the token that grants you access to the OpenAI
   services. Make sure that you copy it to a secure location.

4. **Set the token as an environment variable:** To use the project with your Azure OpenAI
   token, set the token as an environment variable having this name: ``OPEN_AI_TOKEN``.


Additional required environment variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In addition to setting up environment variables for the GitHub access token and Azure OpenAI
token, you must set up some additional environment variables to configure the OpenAI client
and model.

**OPENAI_API_BASE**

* Description: Specifies the endpoint of your Azure OpenAI resource, as shown on its
  **Keys and Endpoint** page. Used only when ``OPENAI_API_TYPE`` is ``azure``.
* Example: ``https://your-resource-name.openai.azure.com``

**OPENAI_API_TYPE**

* Description: Set this variable to ``azure`` to use Azure OpenAI. If it has any other
  value or is not set, the bot uses the standard OpenAI API with ``OPEN_AI_TOKEN`` as the
  API key and ignores ``OPENAI_API_BASE`` and ``OPENAI_API_VERSION``.
* Example: ``azure``

**OPENAI_API_VERSION**

* Description: Indicates the version of the Azure OpenAI API to use. Used only when
  ``OPENAI_API_TYPE`` is ``azure``. If not set, it defaults to ``2023-05-15``.
* Example: ``2023-05-15``

**OPENAI_MODEL**

* Description: Specifies the chat model to use. With Azure OpenAI, this is the name of the
  model deployment in your Azure OpenAI resource. This variable has no default value. It
  is always read from the environment, even when you use a JSON configuration file.
* Example: ``gpt-4o``

With all these environment variables properly configured, you are ready to leverage the full
potential of the review bot.

Optionally, if you are using the review bot through the CLI locally, you can set the OpenAI
variables other than ``OPENAI_MODEL`` in a JSON configuration file as per this example.
Values in this file take precedence over the corresponding environment variables.

.. code-block:: json

   {
      "OPEN_AI_TOKEN": "your-token",
      "OPENAI_API_BASE": "https://your-resource-name.openai.azure.com",
      "OPENAI_API_VERSION": "2023-05-15",
      "OPENAI_API_TYPE": "azure"
   }

CLI usage
---------

The ``reviewbot`` command reviews the changes in a local Git repository. It compares the
working tree with the repository's ``main`` branch and prints the suggestions to the
terminal. To use it, run this command:

.. code:: bash

    reviewbot -r path-to-repo [-c path-to-openai-config]

The command accepts these options:

- ``-r``, ``--review``: Path to the root of the local Git repository to review. The
  repository must have a ``main`` branch.
- ``-c``, ``--config``: Optional path to a JSON configuration file for OpenAI, as described
  in `Additional required environment variables`_.


.. LINKS AND REFERENCES
.. _black: https://github.com/psf/black
.. _flake8: https://flake8.pycqa.org/en/latest/
.. _isort: https://github.com/PyCQA/isort
.. _pip: https://pypi.org/project/pip/
.. _pytest: https://docs.pytest.org/en/stable/
.. _Sphinx: https://www.sphinx-doc.org/en/master/
