import logging
import time
from behave import step
from selenium import webdriver
from tutorial.wikipedia_page import WikipediaPage


@step("I open a browser")
def step_impl(context, maximized=True):
    context.driver = webdriver.Chrome()
    if maximized:
        context.driver.maximize_window()


@step("I navigate to the Wikipedia page")
def step_impl(context):
    context.wikipedia_page = WikipediaPage(context.driver)
    logging.info("Navigating to the Wikipedia page")
    context.wikipedia_page.navigate()


@step("I see in the page '{search_text}'")
def step_impl(context, search_text):
    logging.info("Searching for the text '{}'".format(search_text))
    context.wikipedia_page.search_for(search_text)
    time.sleep(1)
