#!/usr/bin/python
# -*- coding: utf-8 -*-
from unittest.mock import inplace

from flask import Flask, request, render_template
from base.webdriverfactory import WebDriverFactory
import json
import os
import pandas as pd
from base.selenium_drivers import SeleniumDriver
from utilities.teststatus import Status
import utilities.custom_logger as cl
import logging
import time

from werkzeug.utils import secure_filename

app = Flask(__name__)


def createTestSuit(data):
    testCases = []
    data['Predecessor'].fillna(max(sorted(data['Predecessor'])) + 1, inplace=True)
    data['WaitAfterCommand'].fillna(2, inplace=True)
    data['Wait-For-Element'].fillna(2, inplace=True)
    data['Wait-Timeout'].fillna(2, inplace=True)
    data.fillna(0)
    testDone = []
    for test in sorted(data['Predecessor']):
        if test in testDone:
            continue
        else:
            testCases.append([data[data['Predecessor'] == test]])
            testDone.append(test)
    test_cases_result = []
    case_no = 0
    for case in range(len(testCases)):
        for test in range(len(testCases[case][0])):
            data = \
                {"FindElementType": str(testCases[case][0].iloc[test, :]["FindElementType"]).strip(),
                 "ActionCommand": str(testCases[case][0].iloc[test, :]["ActionCommand"]).strip(),
                 "ActionParameters": str(testCases[case][0].iloc[test, :]["ActionParameters"]).strip(),
                 "WaitAfterCommand": str(testCases[case][0].iloc[test, :]["WaitAfterCommand"]).strip(),
                 "Predecessor": str(testCases[case][0].iloc[test, :]["Predecessor"]).strip(),
                 "ActionNo": str(testCases[case][0].iloc[test, :]["ActionNo"]).strip(),
                 "Wait-For-Element": str(testCases[case][0].iloc[test, :]["Wait-For-Element"]).strip(),
                 "Wait-Timeout": str(testCases[case][0].iloc[test, :]["Wait-Timeout"]).strip(),
                 "FindElement": str(testCases[case][0].iloc[test, :]["FindElement"]).strip()
                 }
            test_cases_result.append(data)
            case_no = case_no + 1
    return test_cases_result




class AutomationInterface(SeleniumDriver):
    log = cl.customLogger(logging.DEBUG)
    element = None
    elementType = None
    Action = None
    Data = None
    waitAfterCmd = None
    timeOut = None
    driver = None
    stat = None


    def __init__(self, driver):
        try:
            super(SeleniumDriver).__init__(driver)
        except:
            SeleniumDriver.__init__(self, driver)
        self.driver = driver

    def run_All_testCase(self, testCaseJson, baseURL):

        wdf = WebDriverFactory(self.driver)
        self.driver = wdf.getWebDriverInstance(baseURL=baseURL)
        self.stat = Status(self.driver)


        for test in testCaseJson:
            self.element = test['FindElement']
            self.Action = test['ActionCommand']
            self.elementType = test['FindElementType']
            self.Data = test['ActionParameters']
            self.waitAfterCmd = int(float(test['WaitAfterCommand']))
            self.timeOut = int(float(test['Wait-Timeout']))

            if self.Action == "login":
                email = self.Data.strip().split(",")[0]
                password = self.Data.strip().split(",")[1]
                email_locator = self.element.strip().split(",")[0]
                password_locator = self.element.strip().split(",")[1]
                self.sendKeys(email, email_locator, self.elementType)
                time.sleep(self.waitAfterCmd)
                self.sendKeys(password, password_locator, self.elementType)
                self.waitForElement(self.element, self.elementType, self.timeOut)

            elif self.Action == "isElementPresent":
                result = self.isElementPresent(self.element, self.elementType)
                self.stat.markFinal("Test" + self.element, result, "")


            elif self.Action == "elementClick":
                self.elementClick(self.element, self.elementType)
                time.sleep(self.waitAfterCmd)

            # elif self.Action == "verifyTextContains":
            #     exceptedText = self.getText(self.element, self.elementType)
            #     result = self.util.verifyTextContains(self.Data, exceptedText)
            #     self.stat.markFinal("Test" + self.element, result, "Text Contains")

            elif self.Action == "sendKeys":
                self.sendKeys(self.Data, self.element, self.elementType)
                time.sleep(self.waitAfterCmd)

            elif self.Action == "waitForElement":
                self.waitForElement(self.element, self.elementType, self.timeOut)

            elif self.Action == "isElementPresent":
                result = self.isElementPresent(self.element, self.elementType)
                self.stat.markFinal("Test" + self.element, result, "")

            elif self.Action == "clearField":
                self.clearField(self.element, self.elementType)
                time.sleep(self.waitAfterCmd)

            elif self.Action == "getTitle":
                result = self.getTitle()
                print(result)

            elif self.Action == "isElementDisplayed":
                self.isElementDisplayed(self.element, self.elementType)
                time.sleep(self.waitAfterCmd)

            elif self.Action == "scrollIntoView":
                self.scrollIntoView(self.element, self.elementType)
                time.sleep(self.waitAfterCmd)

            elif self.Action == "mouseHover":
                self.mouseHover(self.element, self.elementType)
                self.waitForElement(self.element, self.elementType, self.timeOut)

            elif self.Action == "mouseClick":
                self.mouseClick(self.element, self.elementType)
                time.sleep(self.waitAfterCmd)

            elif self.Action == "webScroll":
                self.webScroll(self.Data)
                time.sleep(self.waitAfterCmd)

        self.driver.quit()


@app.route('/automate', methods=['GET', 'POST'])
def automate():
    # Logger start here
    logging.basicConfig(filename='emp.log', level=logging.INFO)
    try:
        if request.method == 'POST':
            arResults = []
            if request.form['locators'] != "":
                locators = int(request.form['locators'])
                for i in range(locators):
                    arResults.append(str(i))
                return render_template('index.html', item=arResults)
            else:
                # url = request.form['url'].strip()

                url = request.form['url'].strip()

                files = request.files['file']
                filename = secure_filename(files.filename)
                files.save("/home/bilalikram/PycharmProjects/Automation_Interface/data/" + filename)

                if filename.split(".")[-1] in ["xls", "xlsx"]:
                    dataFrame = pd.read_excel(os.path.join("/home/bilalikram/PycharmProjects/Automation_Interface/data/"
                                                           + filename))
                    test_cases_result = createTestSuit(dataFrame)
                elif filename.split(".")[-1] in ["csv"]:
                    dataFrame = pd.read_csv(os.path.join("/home/bilalikram/PycharmProjects/Automation_Interface/data/"
                                                         + filename))
                    test_cases_result = createTestSuit(dataFrame)
                else:
                    return json.dumps({"error": 1, "message": "invalid file"})

                # Bilal's Code
                obj = AutomationInterface(SeleniumDriver)
                obj.run_All_testCase(test_cases_result, url)

                return json.dumps({"response": test_cases_result})


    except Exception as e:
        logging.info('Error Occured When getting json :' + str(e))
        logging.info('************************************************')
        return json.dumps({"error": 1, "message": "Problem in request method " + str(e)}), 400

    return '''
         <!doctype html>
        <title>Cubix Automation Framework</title>
        <br>
        <h3>Cubix Automation Framework</h3>
        
        <h2>Upload CSV, Excel File containing test cases</h2>
        <form method=post enctype=multipart/form-data>
        <p><input type=text name=url></p>
        Enter URL here : <p><input type=file name=file multiple>
        
        <br><br><br> <h1>OR</h1>
        
        <h2>Or Enter Test Cases Manualy</h2>
        <p>How many Locators You have <input type="text" name="locators">
         <p><input type=submit value=Upload></p>
     
        </form>
        '''


@app.route('/automation', methods=['GET', 'POST'])
def automation():
    # Logger start here
    logging.basicConfig(filename='emp.log', level=logging.INFO)
    try:
        if request.method == 'POST':
            testCase = []
            total = len(request.form)

            url = str(request.form['url']).strip()

            for term in range(0, int(total / 4)):
                print(str(term))
                locator = request.form["locators" + str(term)]
                data = request.form["data" + str(term)]
                action = request.form["Actions" + str(term)]
                locatortype = request.form["LocatorType" + str(term)]
                testCase.append({str(term): {"Locator": locator, "Action": action, "LocatorType": locatortype,
                                             "data": data}})

            # Bilal's Code
            obj = AutomationInterface(BasePage)
            obj.run_All_testCase(testCase, baseURL=url)

            return json.dumps({"response": testCase})

    except Exception as e:
        logging.info('Error Occured When getting json :' + str(e))
        logging.info('************************************************')
        return json.dumps({"error": 1, "message": "Problem in request method " + str(e)}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, threaded=True)
