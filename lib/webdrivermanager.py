import selenium.webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


class WebDriverManager:
    """
    A class to manage the setup and lifecycle of the Selenium WebDriver.
    """
    def __init__(self, headless: bool=True):
        """
        Initializes the WebDriverManager with options for the Selenium WebDriver.

        :param headless: A boolean indicating whether to run the browser in headless mode. Default is True.
        """
        self.options = Options()
        if headless:
            self.options.add_argument('--headless')
            self.options.add_argument('--no-sandbox')
        self.driver = selenium.webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)

    def get_driver(self) -> selenium.webdriver.Chrome:
        """
        Retrieves the initialized Selenium WebDriver instance.
        """
        return self.driver

    def quit(self):
        """
        Quits the Selenium WebDriver, closing all associated windows.
        """
        self.driver.quit()