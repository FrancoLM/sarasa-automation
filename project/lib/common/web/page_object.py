import logging

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class PageObject(object):
    """Base class for Page objects for web-based applications"""

    timeout = 30

    # TODO: Handle StaleElementException problems
    # TODO: Find elements. Wait until elem is not present
    def __init__(self, driver):
        self.driver = driver
        self.driver.set_page_load_timeout(self.timeout)

    def _find_element(self, locator, element, wait=3, retries=3):
        """Find element on page.
        Function retries @retries times, waiting @wait seconds after each iteration"""
        result = None
        for _ in range(retries):
            try:
                result = WebDriverWait(driver, wait).until(lambda x: x.find_element(locator, element))
                logging.debug("Element '{}' found".format(element))
                break
            except (NoSuchElementException, TimeoutException):
                logging.debug("Element could not be found. Retrying...".format(element))
            except Exception as ex:
                logging.exception("An error occurred when trying to find element with ID '{}'".format(element))
                raise
        else:
            logging.debug("Element '{}':'{}' could not be found.".format(locator, element))
        return element

    def find_elements(self, by_locator, locator_value, wait=3, retries=3):
        """Function retries @retries times, waiting @wait seconds after each iteration"""
        # for _ in retries:

    def find_element_by_id(self, element_id, wait=3, retries=3):
        """Function retries @retries times, waiting @wait seconds after each iteration
        By.ID:"""
        # TODO: Support not presence
        return self._find_element(By.ID, element_id, wait, retries)

    def find_element_by_class(self, element_class, wait=3, retries=3):
        """Function retries @retries times, waiting @wait seconds after each iteration
        By.CLASS_NAME:"""
        return self._find_element(By.CLASS_NAME, element_class, wait, retries)

    def find_element_by_xpath(self, element_xpath, wait=3, retries=3):
        """Function retries @retries times, waiting @wait seconds after each iteration
        By.XPATH:"""
        return self._find_element(By.XPATH, element_xpath, wait, retries)

    def find_element_by_link_text(self, link_text, wait=3, retries=3):
        """Function retries @retries times, waiting @wait seconds after each iteration
        By.LINK_TEXT: """
        return self._find_element(By.LINK_TEXT, link_text, wait, retries)


if __name__ == "__main__":
    # TODO: Delete
    driver = webdriver.Chrome()
    pp = PageObject(driver)
    pp.driver.get("https://www.google.com")
    print(pp.find_element_by_id("lst-ib"))
    print(pp.find_element_by_class("gsfi"))
    print(pp.find_element_by_xpath('//*[@id="lst-ib"]'))
    print(pp.find_element_by_link_text("Google Search"))
    pp.driver.close()
