from selenium.webdriver.common.by import By

class PageObject(object):
    """Base class for Page objects for web-based applications"""

    # TODO: Handle StaleElementException problems
    def __init__(self, driver):
        self.driver = driver

    def find_element(self, by_locator, locator, wait=1, retries=3):
        """Find element on page.
        Function retries @retries times, waiting @wait seconds after each iteration"""
        pass

    def find_elements(self, by_locator, locator, wait=1, retries=3):
        pass

    def find_element_by_id(self, element_id):
        pass

    def find_element_by_class(self, element_class):
        pass

    def find_element_by_xpath(self, element_xpath):
        pass

    def find_element_by_link_text(self, link_text):
        pass