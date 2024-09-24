from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import lib.webdrivermanager


class Scraper:
    """
    A class to handle web scraping for downloading files using Selenium.
    """
    def __init__(self, driver: lib.webdrivermanager.WebDriverManager) -> None:
        """
        Initializes the Scraper with the provided WebDriver.

        :param driver: The Selenium WebDriver instance to be used for navigation.
        """
        self.driver = driver

    def navigate_to_page(self, url: str) -> None:
        self.driver.get(url)

    def remove_cookie_banner(self) -> None:
        self.driver.execute_script("var banner = document.getElementById('cookie-container'); if (banner) { banner.parentNode.removeChild(banner); }")

    def click_element(self, element_id: str) -> None:
        WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.ID, element_id))).click()

    def get_download_links(self, group_xpath: str, download_url_prefix: str) -> list[str]:
        group_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, group_xpath))
        )

        WebDriverWait(self.driver, 30).until(
        EC.visibility_of_all_elements_located((By.XPATH, "//*[@id='Censos/Censo_Demografico_1991/Indice_de_Gini']//ul[@role='group']//a"))
    )

        links = group_element.find_elements(By.TAG_NAME, "a")
        download_links = []
        for link in links:
            filename = link.text
            if filename.endswith(".zip"):
                download_links.append(download_url_prefix + filename)
        return download_links