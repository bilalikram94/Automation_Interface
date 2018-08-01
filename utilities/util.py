"""
@package Utilities

util class implementation
All most commonly used utilities should be implemented in this class

Example:
    name = self.util.getUniqueName()
"""
import time
import traceback
import random, string
import utilities.custom_logger as cl
import logging


class Util(object):
    log = cl.customLogger(logging.INFO)

    def sleep(self, sec, info=""):
        """
        Put the program to wait for the specified amount of time
        """
        if info is not None:
            self.log.info("Wait:: '" + str(sec) + "' seconds for " + info)
            try:
                time.sleep(sec)
            except InterruptedError:
                traceback.print_stack()

    def getAlphaNumeric(self, length, type='letters'):
        """
        Get random string of characters

        Parameters:
            length: length of string , number of characters should have
            type: Type of character should have. Default is letters
            provide: lower/upper/digits for different types
        """

        alpha_num = ''
        if type == 'lower':
            case = string.ascii_lowercase
        elif type == 'upper':
            case = string.ascii_uppercase
        elif type == 'digits':
            case = string.digits
        elif type == 'mix':
            case = string.ascii_letters + string.digits
        else:
            case = string.ascii_letters
        return alpha_num.join(random.choices(case) for i in range(length))

    def getUniqueName(self, charCount=10):
        """
        Get a unique name
        """
        return self.getAlphaNumeric(charCount, 'lower')

    def getUniqueNameList(self, listSize=5, itemLength=None):
        """
        Get a list of valid Email IDs
        parameter:
            listSize: Number of names, default is 5 names in a list
            itemLength: It should be a list containing numbers of items equal to the listSize
                        This determines the length of each item in the list -> [1,2,3,4,5]
        """

        nameList = []
        for i in range(0, listSize):
            nameList.append(self.getUniqueName(itemLength[i]))
            return nameList

    def verifyTextContains(self, actualText, expectedText):
        """
        Verify actual text contains expected text string
        Patameters:
            expectedlist = Expected text
            actuallist = Actual text
        """
        self.log.info("Actual Text From Application Web UI -> ::" + actualText)
        self.log.info("Expected Text From Application Web UI -> ::" + expectedText)
        if expectedText.lower() in actualText.lower():
            self.log.info("### Verification Contains !!!")
            return True
        else:
            self.log.error("### VERFICATION DOES NOT CONTAINS !!!")
            return False

    def verifyTextMatch(self, actualList, expectedList):
        """
        Verify Text Match
        Parameters:
            expectedlist = Expected text
            actuallist = Actual text
        """
        return set(expectedList) == set(actualList)

    def verifyListMatch(self, actualList, expectedList):
        """
        Verify actual list contains element from expected list
        Parameters:
            expectedlist = Expected text
            actuallist = Actual text
        """
        length = len(expectedList)
        for i in range(0, length):
            if expectedList[i] not in actualList:
                return False
            else:
                return True
