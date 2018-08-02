from selenium.webdriver.common.by import By
from traceback import print_stack
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
import utilities.custom_logger as cl
import logging
import time
import os


class SeleniumDriver:

    driver = None

    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        self.driver = driver
        self.actions = ActionChains(driver)

    def getTitle(self):
        return self.driver.title.strip()

    def getByType(self, locatorType):
        locatorType = locatorType.lower()
        if locatorType == "id":
            return By.ID
        elif locatorType == "name":
            return By.NAME
        elif locatorType == "xpath":
            return By.XPATH
        elif locatorType == "css":
            return By.CSS_SELECTOR
        elif locatorType == "class":
            return By.CLASS_NAME
        elif locatorType == "link":
            return By.LINK_TEXT
        else:
            self.log.info("Locator type " + locatorType +
                          " not correct/supported")
        return False

    def getElement(self, locator, locatorType="id"):
        element = None
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            element = self.driver.find_element(byType, locator)
            self.log.info("Element found with locator - " + locator + " - locatorType: " + locatorType)
        except:
            self.log.info("Element not found with locator: " + locator + " -  locatorType: " + locatorType)

        return element

    def getElementsList(self, locator, locatorType="id"):
        """
        Get list of elements
        """
        element = None
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            element = self.driver.find_elements(byType, locator)
            self.log.info("Element found with - " + locator + " - locatorType: " + locatorType)
            return True
        except:
            self.log.error("Element List not found with locator - " + locator + " - locatorType" + locatorType)
            return element

    def elementClick(self, locator, locatorType="id", element=None):
        """
        Click on an element ->Modified
        either provide element or a combination of locator and locatorType
        """
        try:
            if locator:
                element = self.getElement(locator, locatorType)
            element.click()
            self.log.info("Clicked on element with locator - " + locator + " - locatorType: " + locatorType)
            return True
        except:
            self.log.error("Cannot click on the element with locator - " + locator + " - locatorType: " + locatorType)
            print_stack()
            return False


    def sendKeys(self, data, locator, locatorType="id", element=None):
        try:
            if locator:  # this means if the locator is not empty
                element = self.getElement(locator, locatorType)
            element.send_keys(data)
            self.log.info("Sent data on element with locator - " + locator +
                          " - locatorType: " + locatorType)
            return True
        except:
            self.log.error("Cannot send data on the element with locator - " + locator +
                           " - locatorType: " + locatorType)
            print_stack()
            return False

    def clearField(self, locator, locatorType="id", element=None):
        """
        Method to clear  text field if populated
        """
        try:
            if locator:
                element = self.getElement(locator, locatorType)
            if element is not None:
                element.clear()
                self.log.info("Text Field cleared by locator - " + locator + " - locatorType: " + locatorType)
                return True
        except:
            self.log.error("Element not found by locator - " + locator + " - locatorType: " + locatorType)
            print_stack()
            return False

    def isElementPresent(self, locator, locatorType="id", element=None):
        try:
            if locator:
                element = self.getElement(locator, locatorType)
            if element is not None:
                self.log.info("Element Found by locator - " + locator + " - locatorType:" + locatorType)
                return True
            else:
                self.log.info("Element not found by locator - " + locator + " - locatorType:" + locatorType)
                return False
        except:
            print("Element not found")
            return False

    def elementPresenceCheck(self, locator, byType):
        try:
            elementList = self.driver.find_elements(byType, locator)
            if len(elementList) > 0:
                self.log.info("Element Found")
                return True
            else:
                self.log.info("Element not found")
                return False
        except:
            self.log.info("Element not found")
            return False

    def waitForElement(self, locator, locatorType="id", timeout="5", pollFrequency=0.5):
        element = None
        try:
            byType = self.getByType(locatorType)
            self.log.info("Waiting for maximum :: " + str(timeout) +
                          " :: seconds for element to be clickable")
            wait = WebDriverWait(self.driver, timeout, poll_frequency=1,
                                 ignored_exceptions=[NoSuchElementException,
                                                     ElementNotVisibleException,
                                                     ElementNotSelectableException])
            element = wait.until(EC.element_to_be_clickable((byType,
                                                             "stopFilter_stops-0")))
            self.log.info("Element appeared on the web page - " + locator)
        except:
            self.log.info("Element not appeared on the web page - " + locator)
            print_stack()
        return element

    def screenShot(self, resultMessage):
        """
        Takes screenshot of the current web page
        """
        fileName = resultMessage + "." + str(round(time.time() * 1000)) + ".png"
        screenshotDirectory = os.getcwd() + "/screenshots/"
        relativeFileName = screenshotDirectory + fileName
        currentDirectory = os.path.dirname(__file__)
        destinationFile = os.path.join(currentDirectory, relativeFileName)
        destinationDirectory = os.path.join(currentDirectory, screenshotDirectory)

        # noinspection PyBroadException
        try:
            if not os.path.exists(destinationDirectory):
                os.makedirs(destinationDirectory)
            self.driver.save_screenshot(destinationFile)
            self.log.info("Screenshot save to directory - " + destinationFile)
        except:
            self.log.error("### Exception Occurred when taking screenshot")
            print_stack()

    def getText(self, locator="", locatorType="id", element=None, info=""):
        """
        New Method
        Get Text on an element
        Either provide element or combination of locator and locatorType
        """
        try:
            if locator:
                self.log.debug("In locator condition")
                element = self.getElement(locator, locatorType)
            self.log.debug("Before Finding Text")
            text = element.text

            self.log.debug("after Finding Text" + str(len(text)))
            if len(text) == 0:
                text = element.get_attribute("inner text")
                text = text.strip()
            if len(text) != 0:
                self.log.info("Getting text on element ::" + info)
                self.log.info("The Text is ::'" + text + "'")
                text = text.strip()
            return True

        except:
            self.log.error("###Failed To Get Text On Element !!!" + info)
            print_stack()
            text = None

        return text, False

    def isElementDisplayed(self, locator="", locatorType="id", element=None):
        """
        New Method
        Check if element is displayed
        Either provide element or combination of locator and locatorType
        """
        isDisplayed = False
        try:
            if locator:
                element = element.getElement(locator, locatorType)
            if element is not None:
                isDisplayed = element.is_displayed()
                self.log.info("Element is displayed with locator - " + locator + " - locatorType" + locatorType)
                return True
            else:
                self.log.error("Element not displayed with locator - " + locator + " - locatorType" + locatorType)
            return isDisplayed
        except:
            print("Element NOT Found")
            return False

    def webScroll(self, direction="up", distance=""):
        """
        NEW METHOD
        """
        if direction == "up":
            # Scroll UP
            self.driver.execute_script("window.scrollBy(0," + distance + ");")

        if direction == "down":
            # Scroll Down
            self.driver.execute_script("window.scrollBy(0," + distance + ");")

    def mouseHover(self, locator, locatorType="id", element=None):
        """
        NEW METHOD
        Mouse Hover on an element
        either provide element or a combination of locator and locatorType
        """
        try:
            if locator:
                element = self.getElement(locator, locatorType)
            if element is not None:
                self.actions.move_to_element(element).perform()
                self.log.info("Element Found by locator - " + locator + " - locatorType:" + locatorType)
                return True
        except:
            self.log.error("Cannot find element with locator - " + locator + " - locatorType: " + locatorType)
            print_stack()
            return False

    def mouseClick(self, locator, locatorType="id", element=None):
        """
                NEW METHOD
                Mouse Hover on an element and click
                either provide element or a combination of locator and locatorType
        """
        try:
            if locator:
                element = self.getElement(locator, locatorType)
            if element is not None:
                self.actions.move_to_element(element).click().perform()
                self.log.info("Clicked on element with locator - " + locator + " - locatorType: " + locatorType)
                return True
        except:
            self.log.error("Cannot click on the element with locator - " + locator + " - locatorType: " + locatorType)
            print_stack()
            return False

    def scrollIntoView(self, locator, locatorType="id", element=None):
        """
                NEW METHOD
                Scrolls Element into View
                either provide element or a combination of locator and locatorType
        """
        try:
            if locator:
                element = self.getElement(locator, locatorType)
            if element is not None:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                self.log.info("Element Scrolled into View with locator - " + locator + " - locatorType: " + locatorType)
                return True
        except:
            self.log.error(
                "### Element NOT Scrolled into View with locator - " + locator + " - locatorType: " + locatorType)
            print_stack()
            return False

    def dragDrop(self, fromlocator, tolocator, fromlocatorType="id", tolocatorType="id"):
        """
        Accepts four parameters fromlocator, fromlocatorType, tolocator, tolocatorType
        provide two combinations of locators and locatorTypes

        example:
            self.dragDrop(fromlocator,tolocator,fromlocatorType,tolocatorType)
        """
        try:
            if fromlocator:
                fromlocator = self.getElement(fromlocator, fromlocatorType)
                tolocator = self.getElement(tolocator, tolocatorType)
            self.actions.click_and_hold(fromlocator).move_to_element(tolocator).release().perform()
            self.log.info("Item dragged from - " + fromlocator + " - FromLocator: " + fromlocatorType)
            self.log.info("Item dragged to - " + tolocator + " - ToLocator:" + tolocatorType)
            return True

        except:
            self.log.error("Element not found with locator - " + fromlocator + " - locatorType: " + fromlocatorType)
            self.log.error("Element not found with locator - " + tolocator + " - locatorType: " + tolocatorType)
            print_stack()
            return False

    def windowSize(self):
        try:
            height = self.driver.execute_script("return window.innerHeight;")
            width = self.driver.execute_script("return window.innerWidth;")
            self.log.info("Height of Current Window is - " + height + " - Width of Current Window is: " + width)
            return True

        except:
            self.log.error("###Could not measure Height and Width !!!")
            print_stack()
            return False

    def dropDownList(self, locator, locatorType="id", val="", element=None):
        """
        Accepts three parameters locator, locatorType and val
        selects from drop down list
        by default val is set to 'index'
        Example:
             self.dropDownList(locator, locatorType, val="value")
        """
        try:
            sel = Select(element)
            if locator:
                element = self.getElement(locator, locatorType)
            if element is not None:
                sel.select_by_index(val)
                self.log.info("Element selected from list by Index - " + val)
            elif val == "value":
                self.log.info("Element selected from list by Value - " + val)
                return sel.select_by_value(val)
            else:
                sel.select_by_visible_text(val)
                self.log.info("Element selected from list by Visible Text - " + val)
            return True

        except:
            self.log.error("### Can NOT find Element with locator - " + locator + " - locatorType: " + locatorType)
            self.log.error("### Can't select value: " + val)
            return False

    def driverWaitImplicitly(self, waitAfterCommand):
        try:
            self.driver.implicitlyWait(waitAfterCommand)
            self.log.info("Driver waited for:" + waitAfterCommand)
            return True
        except:
            self.log.error("Could not wait for" + waitAfterCommand)
            return False
