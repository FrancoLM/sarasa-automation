Slayer Framework Tutorial
=========================


Slayer makes use of the Behave Python library to run test cases.
So, very much like Behave, Slayer will look for a folder called "features" and a
"steps" sub-folder inside it for feature files and the steps implementation, respectively.
You can consult the `Behave documentation <http://behave.readthedocs.io/en/latest/>`_ for more information.

Tutorial
========

Let's go trough a simple example. Let's create a test that opens the Wikipedia webpage and searches for the term
"Behavior Driven Development"

* Import Slayer in your project
* Install the Chrome webdriver
* Create a WikipediaPage class, that we'll use to automate our test. In the root of your project create a Python script "wikipedia_page.py":

.. literalinclude:: ../tutorial/wikipedia_page.py
    :language: python


* Add a new directory called "features" in your root, and create a file "wikipedia.feature", and paste the following:

.. literalinclude:: ../tutorial/wikipedia.feature
    :language: gherkin


* Add a new directory "steps" inside "features", and create a Python script "tutorial_steps.py":

.. literalinclude:: ../tutorial/tutorial_steps.py
    :language: python


* In your main script, import Slayer and run it:

.. literalinclude:: ../tutorial/run_slayer_script.py
    :language: python


And that's it! Slayer runs your test!
You will find the output for the execution inside the "output" folder that Slayer creates automatically.

Modifying the Slayer execution
==============================

Slayer uses configuration files to setup the execution options. These options include output folders, logging format,
and proxy compatibility. The default Slayer configuration files are shown below.

Slayer configuration: config.cfg
--------------------------------

.. literalinclude:: ../slayer/config/config.cfg
    :language: cfg


Slayer logging: logger.yaml
---------------------------

.. literalinclude:: ../slayer/config/logger.yaml
    :language: yaml


Provide your own configuration files to Slayer
----------------------------------------------


The config.cfg and logger.yaml files describe the default behavior for Slayer. But you can change Slayer works by
providing the path and filename for your own configuration and logger files, by providing any of these two arguments
in your execution.

.. code-block:: bash

    <execution command> --framework-config <custom_config_file> --logs-config <custom_logger_file>


For example, if your main script is called main.py, and your configuration files are called "my_config.cfg" and
"my_logger.yaml":

.. code-block:: bash

    python main.py --framework-config my_config.cfg --logs-config my_logger.yaml


Slayer will run, but instead of using the default configuration, it will use your own configuration files.

.. note::
    The logger file specifies the options for the Python default logger. The options defined are read as a dict
    and passed as option in a logging.config.dictConfig call. Please refer to the
    `logging configuration <https://docs.python.org/2/library/logging.config.html>`_ for more details and available options


Behave execution
----------------

Slayer configures the behave execution before running the tests. But this configuration can be overridden by providing
the framework with a behave.ini file. The default file define the following options:

.. literalinclude:: ../slayer/behave.ini
    :language: ini


In effect, all options defined in this file are default behave options.

If you want to define your own options, create a file called "behave.ini", and provide Slayer with the path to this file:
Following the previous example:

.. code-block:: bash

    python main.py --behave-config <path_to_behave_ini_file>


By default, Slayer will look for the "behave.ini" file in the same folder your main script is located, so you do not need
to use this argument if your ini file is located there.

.. note::
    Refer to the `Behave Parameters documentation
    <https://behave.readthedocs.io/en/latest/behave.html#configuration-parameter-types>`_
    for information on available parameters.
