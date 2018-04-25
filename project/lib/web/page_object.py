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
        return self._element_finder[by_locator](locator_value, wait, retries)

    def find_elements(self, by_locator, locator_value, wait=1, retries=3):
        """Function retries @retries times, waiting @wait seconds after each iteration"""
        for _ in retries:
            

    def _find_element_by_id(self, element_id):
        """Function retries @retries times, waiting @wait seconds after each iteration"""
        pass

    def _find_element_by_class(self, element_class):
        """Function retries @retries times, waiting @wait seconds after each iteration"""
        pass

    def _find_element_by_xpath(self, element_xpath):
        """Function retries @retries times, waiting @wait seconds after each iteration"""
        pass

    def _find_element_by_link_text(self, link_text):
        pass

    _element_finder = {
        By.ID:          _find_element_by_id,
        By.CLASS_NAME:  _find_element_by_class,
        By.XPATH:       _find_element_by_xpath,
        By.LINK_TEXT:   _find_element_by_link_text
    }
