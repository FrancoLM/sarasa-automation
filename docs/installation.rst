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

.. code-block:: python

   import time
   from selenium import webdriver
   from selenium.webdriver.common.by import By
   from slayer.lib.common.web.page_object import PageObject

   class WikipediaPage(PageObject):
       url = "https://www.wikipedia.org"
       # Locators
       page_title = (By.CLASS_NAME, "svg-Wikipedia_wordmark")
       search_bar = (By.ID, "searchInput")
       search_button = (By.XPATH, '//*[@id="search-form"]/fieldset/button')
       search_result_title = (By.XPATH, '//*[@id="firstHeading"]')

       def __init__(self, web_driver):
           super().__init__(web_driver)

       def _validate_page(self):
           self.find_element(*self.page_title)

       def search_for(self, query):
           self.find_element(*self.search_bar).send_keys(query)
           self.find_element(*self.search_button).click()
           time.sleep(1)

       def get_search_result_title(self):
           return self.find_element(*self.search_result_title).text


* Add a new directory called "features" in your root, and create a file "example.feature", and paste the following:

.. code-block:: gherkin

   Feature: A simple Slayer project
   Scenario: My first Slayer test
     Given I open a browser
     Given I navigate to the Wikipedia page
     When I search for the text 'Behavior Driven Development'
     Then I see the page for 'Behavior-driven development'


* Add a new directory "steps" inside "features", and create a Python script "example_steps.py":

.. code-block:: python

   import logging
   from selenium import webdriver
   from behave import step
   from wikipedia_page import WikipediaPage


   @step("I open a browser")
   def step_impl(context, maximized=True):
       context.driver = webdriver.Chrome()
       if maximized:
           context.driver.maximize_window()


   @step("I navigate to the Wikipedia page")
   def step_impl(context):
       context.wikipedia_page = WikipediaPage(context.driver)
       logging.info("Navigating to the WIkipedia page")
       context.wikipedia_page.navigate()


   @step("I search for the text '{search_text}'")
   def step_impl(context, search_text):
       logging.info("Searching for the text '{}'".format(search_text))
       context.wikipedia_page.search_for(search_text)
       time.sleep(1)


   @step("I see the page for '{page_title}'")
   def step_impl(context, page_title):
       assert context.wikipedia_page.get_search_result_title() == page_title


* In your main script, import Slayer and run it:

.. code-block:: python

   from slayer import run_framework
   run_framework()


And that's it! Slayer runs your test!
You will find the output for the execution inside the "output" folder that Slayer creates automatically.

Modifying the Slayer execution
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
In progress
