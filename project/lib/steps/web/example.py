import time
from behave import *
from selenium import webdriver


@step("I open a browser")
def step_impl(context):
    context.driver = webdriver.Chrome()
    context.driver.maximize_window()

@step("I go to the Google web page")
def step_impl(context):
    context.driver.get("https://www.google.com")
    time.sleep(5)
