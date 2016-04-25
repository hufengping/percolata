# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains
import unittest, time, re,os,string
from public import Autotest
import xml.dom.minidom

#get time now
now = time.strftime("%Y-%m-%d_%H_%M_%S")
tdata=  time.strftime("%Y-%m-%d")
class TestCase_01(unittest.TestCase):
    u'''部分领取'''

    @classmethod
    def  setUpClass(cls):
        cls.driver = webdriver.Firefox()
        cls.driver.implicitly_wait(30)
        #print self.base_url
        cls.verificationErrors = []
        cls.accept_next_alert = True
    def  setUp(self):
        pass
    
    def test_01_login(self):
        u'''login'''
        driver = self.driver
        driver.get("http://manager.percolata.com/")
        logins = root.getElementsByTagName('user')
        #获得null 标签的username、passwrod 属性值
        username=logins[0].getAttribute("username")
        password=logins[0].getAttribute("password")
        prompt_info = logins[0].firstChild.data
        #登录
        Autotest.login(self,username,password)
        #获取断言信息进行断言
        text = driver.find_element_by_xpath("/html/body/div[2]/div/div[3]/div/div[2]/div/table/tbody/tr/td").text
        try:
            self.assertEqual(text,prompt_info,U'登录信息验证失败，请检查网络或登录信息！')
        except AssertionError,e:
            print e
            print ' 请查看截图文件 '+now+'.png'
            driver.get_screenshot_as_file(xmlpath2+"log\\"+now+U'登录信息验证不通过.png')#如果没有找到上面的元素就截取当前页面。

            
       
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def is_alert_present(self):
        try: 
            self.driver.switch_to_alert()
        except NoAlertPresentException, e: 
            print e
            return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

    def tearDown(self):
        self.assertEqual([], self.verificationErrors)
        
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
