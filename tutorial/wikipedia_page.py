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

    def __init__(self, webdriver):
        super().__init__(webdriver)

    def _validate_page(self):
        self.find_element(*self.page_title)

    def search_for(self, query):
        self.find_element(*self.search_bar).send_keys(query)
        self.find_element(*self.search_button).click()
        time.sleep(1)

    def get_search_result_title(self):
        return self.find_element(*self.search_result_title).text
