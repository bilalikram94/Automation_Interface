"""
@package utilities

CheckPoint class implementation
It provides functionality to assert the result

Example:
    self.check_point.markFinal("Test Name", result, "Message")
"""
import utilities.custom_logger as cl
import logging
from base.selenium_drivers import SeleniumDriver
import allure
from traceback import print_stack


class Status(SeleniumDriver):
    log = cl.customLogger(logging.INFO)

    def __init__(self, driver):
        """
        Inits CheckPoint class
        """
        try:
            super().__init__(driver)
        except:
            SeleniumDriver.__init__(self, driver)
        self.resultList = []

    def setResult(self, result, resultMessage):
        try:
            if result is not None:
                if result:
                    self.resultList.append("PASS")
                    self.log.info("### VERIFICATION SUCCESSFUL :: + " + resultMessage)
                else:
                    self.resultList.append("FAIL")
                    self.log.error("### VERIFICATION FAILED :: + " + resultMessage)
                    res = self.screenShot(resultMessage)
                    allure.attach.file(res, resultMessage, attachment_type=allure.attachment_type.PNG)
            else:
                self.resultList.append("FAIL")
                self.log.error("### VERIFICATION FAILED :: + " + resultMessage)
                res = self.screenShot(resultMessage)
                allure.attach.file(res, resultMessage, attachment_type=allure.attachment_type.PNG)
        except:
            self.resultList.append("FAIL")
            self.log.error("### Exception Occurred !!!")
            res = self.screenShot(resultMessage)
            allure.attach.file(res, resultMessage, attachment_type=allure.attachment_type.PNG)
            print_stack()

    def mark(self, result, resultMessage):
        """
        Mark the result of the verification point in a test case
        """
        self.setResult(result, resultMessage)

    def markFinal(self, testName, result, resultMessage):
        """
        Mark the final result of the verification point in a test case
        This needs to be called at least once in a test case
        This should be final test status of the test case
        """
        self.setResult(result, resultMessage)

        if "FAIL" in self.resultList:
            self.log.error(testName + " ### TEST FAILED")
            self.resultList.clear()
            assert True == False
        else:
            self.log.info(testName + " ### TEST SUCCESSFUL")
            self.resultList.clear()
            assert True == True
