# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains
import unittest, time, re,os,string
from public import Autotest,db2file
import xml.dom.minidom

#打开XML文档
xmlpath = os.path.split(os.path.realpath(__file__))[0] #获取当前路径
xmlpath2 = xmlpath.split('src')[0]
dom = xml.dom.minidom.parse(xmlpath2+'testdata\\config.xml')
#得到文档元素对象
root = dom.documentElement

#获取当前时间
now = time.strftime("%Y-%m-%d_%H_%M_%S")
tdata=  time.strftime("%Y-%m-%d")
barcode = '1111020003808413'   #存储条形码
class TestCase_01(unittest.TestCase):
    u'''生产个险渠道条形码'''

    @classmethod
    def  setUpClass(cls):#所有用例执行前，执行
        cls.driver = webdriver.Firefox()
        cls.driver.implicitly_wait(30)
        cls.verificationErrors = []
        cls.accept_next_alert = True
        logins = root.getElementsByTagName('url_barcode')
        cls.base_url = logins[0].firstChild.data
        print cls.base_url
        
    def  setUp(self):#每条用例执行前，执行
        pass
    
    def test_01_getbarcode(self):
        u'''选择INT2环境，个险渠道'''
        driver = self.driver
        driver.get(self.base_url)
        try:
        #切换到相应iframe

            driver.switch_to_frame(driver.find_element_by_xpath('/html/body/table[2]/tbody/tr/td[2]/table/tbody/tr/td/iframe'))
            #获取断言信息进行断言
            text = driver.find_element_by_xpath("/html/body/table[1]/tbody/tr[1]/td/div/li/strong").text

            self.assertEqual(text,u'新投保单号生成')
        except Exception,e:
            print e
            print u"测试文档库被关闭，请打开后重新运行测试！"
            print ' 测试文档库被关闭'+now+'.png'
            driver.get_screenshot_as_file(xmlpath2+"log\\"+now+U'测试文档库被关闭.png')#如果没有找到上面的元素就截取当前页面。
            
        #请选择测试环境:INT2
        driver.find_element_by_xpath("//input[@value='INT2']").click()
        #请选择渠道类型:个险渠道
        driver.find_element_by_xpath("//input[@value='1111']").click()
        #投保单号生成
        driver.find_element_by_xpath("//input[@value='投保单号生成']").click()
        #保存投保单号
        barcode = driver.find_element_by_xpath("/html/body/div/div[2]/table/tbody/tr[2]/td/font").text
        print "个险渠道条形码： %d" %barcode
        #返回主frame 
        driver.switch_to_default_content()
        
        
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def is_alert_present(self):
        try: 
            self.driver.switch_to_alert()
        except NoAlertPresentException, e: 
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

    def tearDown(self):#每条用例执行完，执行
        self.assertEqual([], self.verificationErrors)
        
    @classmethod #所有用例执行完，执行
    def tearDownClass(cls):
        cls.driver.quit()
        #pass

        
        
if __name__ == "__main__":
    unittest.main()
