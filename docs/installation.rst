Installing Slayer
=================

Requirements:
^^^^^^^^^^^^^

* Python 3.x (Python >= 3.6 recommended)
* For web automation, make sure you have a webdriver downloaded in your system, and it's added to your PATH (Windows).


Projects like `Selenium <https://www.seleniumhq.org/>`_ automate web browsers, and the Python library provided by
this project is used in Slayer. Refer to their documentation for more information.


Installing the Framework
^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: bash

    pip install slayer


Running the Framework
^^^^^^^^^^^^^^^^^^^^^

Slayer, very much like the Behave Python library it's based on, will look for a folder called "features" and a
"steps" sub-folder inside it for feature files and the steps implementation, respectively.
You can consult the `Behave documentation <http://behave.readthedocs.io/en/latest/>`_ for more information.

Let's go trough a simple example. Let's create a test that opens the Wikipedia webpage and searches for the term
"Behavior Driven Development"

* Import Slayer in your project
* Install the Chrome webdriver
* Create a WikipediaPage class, that we'll use to automate our test. In the root of your project create a Python script "wikipedia_page.py":

.. literalinclude:: ..\tutorial\wikipedia_page.py
    :language: python


* Add a new directory called "features" in your root, and create a file "wikipedia.feature", and paste the following:

.. literalinclude:: ..\tutorial\wikipedia.feature
    :language: gherkin


* Add a new directory "steps" inside "features", and create a Python script "tutorial_steps.py":

.. literalinclude:: ..\tutorial\tutorial_steps.py
    :language: python


* In your main script, import Slayer and run it:

.. literalinclude:: ..\tutorial\run_slayer_script.py
    :language: python


And that's it! Slayer runs your test!
You will find the output for the execution inside the "output" folder that Slayer creates automatically.

Modifying the Slayer execution
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
In progress
