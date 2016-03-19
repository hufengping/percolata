# -*- coding: utf-8 -*-
#!/usr/bin/env python
''' 
  @author:      Zhiwei Yang
  @dateTime:    2015-12-14
'''
import unittest
import os
from appium import webdriver
from time import sleep
import json

jim = "jim@gmail.com"
with open ("config.json") as f:
    config_data = json.load(f)
    xpath = config_data['iosxpath']

class SimpleIOSTests(unittest.TestCase):

    def setUp(self):
        # set up appium
        app = os.path.join(os.path.dirname(__file__),
                           config_data['iOSPath'])
        app = os.path.abspath(app)
        self.driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4723/wd/hub',
            desired_capabilities={
                'app': 'com.happypoly.yang.staffum',
                'platformName': 'iOS',
                'platformVersion': '9.2',
                'udid':'c370276f969060a2dcf0965c9d2992522e26555c',  # The real iphone's uuid
                #'deviceName': 'iPhone 6'
                'deviceName': 'iPhone (9.2)'
            })

    def tearDown(self):
        #self.driver.quit()
        pass
        print "test pass under 80f9ae009f9906bdb97707dbbc963086f339d685"

    def test_login(self):

        els = [self.driver.find_element_by_xpath(xpath[0]['username']),
        self.driver.find_element_by_xpath(xpath[0]['password']),self.driver.find_element_by_xpath(xpath[0]['signin'])]
        sleep(15)
        els[0].send_keys(jim)
        self.driver.hide_keyboard()
        els[1].send_keys("qwerty")
        sleep(1)
        els[2].click()
        sleep(15)



if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SimpleIOSTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
