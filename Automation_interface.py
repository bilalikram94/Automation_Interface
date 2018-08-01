#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
from flask import Flask, request, render_template
from base.webdriverfactory import WebDriverFactory
import json
import pickle
import joblib
import os
import pandas as pd
from base.basepage import BasePage
import utilities.custom_logger as cl
import logging
from utilities.read_data import getCVSData
import time

from werkzeug.utils import secure_filename

app = Flask(__name__)


class LoginPage(BasePage):
    log = cl.customLogger(logging.DEBUG)
    locator = None
    locatorType = None
    Action = None
    Data = None

    def __init__(self, driver):
        try:
            super(BasePage).__init__(driver)
        except:
            BasePage.__init__(self, driver)
        self.driver = driver

    def run_All_testCase(self, testCaseJson, baseURL):

        wdf = WebDriverFactory(self.driver)
        self.driver = wdf.getWebDriverInstance(baseURL=baseURL)

        for test in testCaseJson:
            self.locator = testCaseJson[test]['Locator']
            self.Action = testCaseJson[test]['Action']
            self.locatorType = testCaseJson[test]['LocatorType']
            self.Data = testCaseJson[test]['data']

            if self.Action == "login":
                email = self.Data.strip().split(",")[0]
                password = self.Data.strip().split(",")[1]
                email_locator = self.locator.strip().split(",")[0]
                password_locator = self.locator.strip().split(",")[1]
                self.sendKeys(email, email_locator, self.locatorType)
                time.sleep(3)
                self.sendKeys(password, password_locator, self.locatorType)
                time.sleep(3)

            elif self.Action == "isElementPresent":
                self.isElementPresent(self.locator, self.locatorType)

            elif self.Action == "elementClick":
                self.elementClick(self.locator, self.locatorType)

            elif self.Action == "verifyTextContains":
                exceptedText = self.getText(self.locator, self.locatorType)
                result = self.util.verifyTextContains(self.Data, exceptedText)
                self.stat.markFinal(baseURL, result, "Text Contains")

            elif self.Action == "sendKeys":
                self.sendKeys(self.Data, self.locator, self.locatorType)
                time.sleep(3)

            elif self.Action == "waitForElement":
                self.waitForElement(self.locator, self.locatorType)

            elif self.Action == "isElementPresent":
                result = self.isElementPresent(self.locator, self.locatorType)
                self.stat.markFinal(baseURL, result, "")

            elif self.Action == "clearField":
                self.clearField(self.locator, self.locatorType)

            elif self.Action == "getTitle":
                self.getTitle()

            elif self.Action == "isElementDisplayed":
                self.isElementDisplayed(self.locator, self.locatorType)

            elif self.Action == "scrollIntoView":
                self.scrollIntoView(self.locator, self.locatorType)

            elif self.Action == "mouseHover":
                self.mouseHover(self.locator, self.locatorType)
                time.sleep(2)

            elif self.Action == "mouseClick":
                self.mouseClick(self.locator, self.locatorType)

            elif self.Action == "webScroll":
                self.webScroll(self.Data)

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
                url = request.form['url'].strip()

                url = request.form['url'].strip()

                files = request.files['file']
                filename = secure_filename(files.filename)
                files.save("/home/bilalikram/PycharmProjects/Automation_Interface/data/" + filename)

                if filename.split(".")[-1] in ["xls", "xlsx"]:
                    dataFrame = pd.read_excel(os.path.join("/home/bilalikram/PycharmProjects/Automation_Interface/data/"
                                                           + filename))
                elif filename.split(".")[-1] in ["csv"]:
                    dataFrame = pd.read_csv(os.path.join("/home/bilalikram/PycharmProjects/Automation_Interface/data/"
                                                         + filename))
                else:
                    return json.dumps({"error": 1, "message": "invalid file"})

                locators = list(dataFrame['Locator'])
                locatorTypes = list(dataFrame['LocatorType'])
                actions = list(dataFrame['Action'])
                data = list(dataFrame['Data'])
                predecessor = list(dataFrame['Predecessor'])
                actionNo = list(dataFrame['Action No'])
                waitForElement = list(dataFrame['Wait For Element'])
                waitTimeout = list(dataFrame['Wait Timeout'])
                actionParameters = list(dataFrame['Action Parameters'])
                waitAfterCommand = list(dataFrame['Wait After Command'])

                testCase = {}

                for term in range(len(locators)):
                    print(str(term))
                    testCase.update({str(term): {"Locator": locators[term], "Action": actions[term],
                                                 "LocatorType": locatorTypes[term], "data": data[term],
                                                 "Predecessor": predecessor[term], "Action No": actionNo[term],
                                                 "Wait For Element": waitForElement[term],
                                                 "Wait Timeout": waitTimeout[term],
                                                 "Action Parameters": actionParameters[term],
                                                 "Wait After Command": waitAfterCommand[term]}})

                # Bilal's Code
                obj = LoginPage(BasePage)
                obj.run_All_testCase(testCase, url)

                return json.dumps({"response": testCase})


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
            testCase = {}
            total = len(request.form)

            url = str(request.form['url']).strip()

            for term in range(0, int(total / 4)):
                print(str(term))
                locator = request.form["locators" + str(term)]
                data = request.form["data" + str(term)]
                action = request.form["Actions" + str(term)]
                locatortype = request.form["LocatorType" + str(term)]
                testCase.update({str(term): {"Locator": locator, "Action": action, "LocatorType": locatortype,
                                             "data": data}})

            # Bilal's Code
            obj = LoginPage(BasePage)
            obj.run_All_testCase(testCase, baseURL=url)

            return json.dumps({"response": testCase})

    except Exception as e:
        logging.info('Error Occured When getting json :' + str(e))
        logging.info('************************************************')
        return json.dumps({"error": 1, "message": "Problem in request method " + str(e)}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, threaded=True)
