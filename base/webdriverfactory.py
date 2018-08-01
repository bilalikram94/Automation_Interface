"""
@package base
WebDriver Factory class implementation
It creates a webdriver instance based on browser configurations

    Example:
        wdf = WebDriverFactory(driver)
        wdf.getWebDriverInstance()

Is called in conftest file instead of Selenium Webdriver

"""


from selenium import webdriver


class WebDriverFactory:

    def __init__(self, browser):
        self.browser = browser
        """
        Inits WebDriverFactory class

        Returns:
            None

        """

    """
    
        Set Chrome driver and iexplorer environment based on OS
        
    """

    def getWebDriverInstance(self, baseURL):
        """
        Get WebDriver Instance based  on the browser configurations
        :return:
            'WebDriver Instance'
        """

        if self.browser == "iexplorer":

            # Set IE Driver

            driver = webdriver.Ie()
        elif self.browser == "firefox":
            driver = webdriver.Firefox()

        else:
            driver = webdriver.Chrome("/usr/bin/chromedriver")

        # Setting Driver Implicit Time Out for an Element

        driver.implicitly_wait(3)

        # Maximize Window

        driver.maximize_window()

        # Loading Browser with App URL

        driver.get(baseURL)
        return driver
