import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from lib.common.web.page_object import PageObject


class WikipediaPage(PageObject):
    url = "https://www.wikipedia.org"
    # Locators
    page_title = (By.CLASS_NAME, "svg-Wikipedia_wordmark")
    search_bar = (By.ID, "searchInput")
    search_button = (By.XPATH, '//*[@id="search-form"]/fieldset/button')

    def __init__(self, web_driver):
        super().__init__(web_driver)

    def _validate_page(self):
        self.find_element(*self.page_title)

    def search_for(self, query):
        self.find_element(*self.search_bar).send_keys(query)
        self.find_element(*self.search_button).click()
        time.sleep(1)


if __name__ == "__main__":
    web_driver = webdriver.Chrome()
    page = WikipediaPage(web_driver)
    page.navigate()
    page.search_for("Hello")
    web_driver.close()
