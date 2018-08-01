#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
from flask import Flask, request, render_template
import json
import pickle
import joblib

app = Flask(__name__)


from base.basepage import BasePage
import utilities.custom_logger as cl
import logging
import time
from ddt import ddt, data, unpack
from utilities.read_data import getCVSData


class LoginPage(BasePage):
    log = cl.customLogger(logging.DEBUG)
    locator = None
    locatorType = None
    Action = None
    Data = None

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def run_all_testCase(self, testCaseJson):

        for test in testCaseJson:
            self.locator = testCaseJson[test]['Locator']
            self.Action = testCaseJson[test]['Action']
            self.locatorType = testCaseJson[test]['LocatorType']
            self.Data = testCaseJson[test]['data']

            if self.Action == "login":
                id = self.Data.strip().split(",")[0]
                password = self.Data.strip().split(",")[1]
                self.sendKeys(id, self.locator, self.locatorType)
                self.sendKeys(password, self.locator, self.locatorType)

            elif self.Action == "isElementPresent":
                self.isElementPresent(self.locator, self.locatorType)

            elif self.Action == "elementClick":
                self.elementClick(self.locator, self.locatorType)

            elif self.Action == "verifyTextContains":
                exceptedText = self.getText(self.locator, self.locatorType)
                result = self.util.verifyTextContains(self.Data, exceptedText)




@app.route('/automate', methods=['GET', 'POST'])
def automate():
    # Logger start here
    logging.basicConfig(filename='emp.log', level=logging.INFO)
    try:
        if request.method == 'POST':
            arResults = []
            locators = int(request.form['locators'])
            for i in range(locators):
                arResults.append(str(i))
            return render_template('index.html', item=arResults)

    except Exception as e:
        logging.info('Error Occured When getting json :' + str(e))
        logging.info('************************************************')
        return json.dumps({"error": 1, "message": "Problem in request method " + str(e)}), 400

    return '''
         <!doctype html>
        <title>Cubix Automation Framework</title>
        <br>
        <h3>Cubix Automation Framework</h3>
        <form method=post enctype=multipart/form-data>
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

            for term in range(0,int(total/4)):
                print(str(term))
                l = request.form["locators" + str(term)]
                d = request.form["data" + str(term)]
                a = request.form["Actions" + str(term)]
                lt = request.form["LocatorType" + str(term)]
                testCase.update({str(term) : {"Locator" : l, "Action":a, "LocatorType":lt, "data":d}})

            # Bilal's Code
            obj = LoginPage()
            obj.run_all_testCase(testCase)
            return json.dumps({"response":testCase})

    except Exception as e:
        logging.info('Error Occured When getting json :' + str(e))
        logging.info('************************************************')
        return json.dumps({"error": 1, "message": "Problem in request method " + str(e)}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, threaded=True)