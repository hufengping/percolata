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
import random

screenshot_path = "C:\\Users\\zhiwei\\percolata\\qa\\StoreAssociate_autotest\\report\\screenshot"
with open ("C:\\Users\\zhiwei\\percolata\\qa\\StoreAssociate_autotest\\config.json") as f:
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
        desired_caps['app'] = PATH(
            '%s' % config_data['AndroidPath']
        )

        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    def tearDown(self):
        # end the session
        self.driver.quit()

    def test_clickhome(self):
        sleep(15)
        self.driver.find_element_by_xpath("%s" % xpath[0]['username']).send_keys("beta5@calendar.percolata.com")
        self.driver.hide_keyboard()
        self.driver.find_element_by_xpath("%s" % xpath[0]['password'] ).send_keys("qqqqqq")
        self.driver.hide_keyboard()
        self.driver.find_element_by_xpath("%s" % xpath[0]['signin'] ).click()

        sleep(10)
        self.driver.find_element_by_xpath("%s" % xpath[0]['homemonth']).click()
        sleep(2)
        self.driver.get_screenshot_as_file("%s\\%s.png"%(screenshot_path,random.randint(1,1000)))

        sleep(10)
        self.driver.find_element_by_xpath("%s" % xpath[0]['homemonth']).click()
        sleep(5)
        self.driver.get_screenshot_as_file("%s\\%s.png"%(screenshot_path,random.randint(1,1000)))

        sleep(10)
        self.driver.find_element_by_xpath("%s" % xpath[0]['TopRighticon']).click()
        sleep(2)
        self.driver.get_screenshot_as_file("%s\\%s.png"%(screenshot_path,random.randint(1,1000)))

        sleep(10)
        self.driver.find_element_by_xpath("%s" % xpath[0]['TopRighticon']).click()
        self.driver.get_screenshot_as_file("%s\\%s.png"%(screenshot_path,random.randint(1,1000)))
        sleep(10)
        self.driver.find_element_by_xpath("%s" % xpath[0]['swapshiftbutton']).click()
        sleep(2)
        self.driver.get_screenshot_as_file("%s\\%s.png"%(screenshot_path,random.randint(1,1000)))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SimpleAndroidTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
