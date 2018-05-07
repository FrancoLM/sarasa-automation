from selenium.webdriver.common.by import By

class PageObject(object):
    """Base class for Page objects for web-based applications"""



    # TODO: Handle StaleElementException problems
    # TODO: Find elements
    def __init__(self, driver):
        self.driver = driver

    def find_element(self, by_locator, locator_value, wait=1, retries=3):
        """Find element on page.
        Function retries @retries times, waiting @wait seconds after each iteration"""
        return self._element_finder[by_locator.upper()](locator_value, wait, retries)

    def find_elements(self, by_locator, locator_value, wait=1, retries=3):
        """Function retries @retries times, waiting @wait seconds after each iteration"""
        # for _ in retries:

    def _find_element_by_id(self, element_id, wait=1, retries=3):
        """Function retries @retries times, waiting @wait seconds after each iteration
        By.ID:"""
        pass

    def _find_element_by_class(self, element_class, wait=1, retries=3):
        """Function retries @retries times, waiting @wait seconds after each iteration
        By.CLASS_NAME:"""
        pass

    def _find_element_by_xpath(self, element_xpath, wait=1, retries=3):
        """Function retries @retries times, waiting @wait seconds after each iteration
        By.XPATH:"""
        pass

    def _find_element_by_link_text(self, link_text, wait=1, retries=3):
        """Function retries @retries times, waiting @wait seconds after each iteration
        By.LINK_TEXT: """
        pass

    _element_finder = {
        "ID":     _find_element_by_id,
        "CLASS":  _find_element_by_class,
        "XPATH":  _find_element_by_xpath,
        "TEXT":   _find_element_by_link_text
    }
