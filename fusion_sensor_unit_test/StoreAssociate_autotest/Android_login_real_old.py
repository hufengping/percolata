# -*- coding: utf-8 -*-
#!/usr/bin/env python
''' 
  @author:      Zhiwei Yang
  @dateTime:    2015-12-15
'''
import os
from time import sleep
import unittest
from appium import webdriver
import json

with open ("config.json") as f:
    config_data = json.load(f)
    xpath = config_data['xpath']

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

class SimpleAndroidTests(unittest.TestCase):
    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '5.1'
        desired_caps['deviceName'] = 'Android Emulator'
        desired_caps['app'] = PATH(config_data['AndroidPath'])

        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    def tearDown(self):
        # end the session
        #self.driver.quit()
        print "test pass under 80f9ae009f9906bdb97707dbbc963086f339d685"
        pass


    def test_find_elements(self):
        sleep(15)
        self.driver.find_element_by_xpath(xpath[0]['username']).send_keys("jim@gmail.com")
        self.driver.hide_keyboard()
        self.driver.find_element_by_xpath(xpath[0]['password'] ).send_keys("qwerty")
        self.driver.hide_keyboard()
        self.driver.find_element_by_xpath(xpath[0]['signin'] ).click()
        sleep(10)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SimpleAndroidTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
