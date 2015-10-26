# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains
import test_unittest, time, re,os,string
from public import Autotest,db2file
from testsuite_01 import *
import xml.dom.minidom
import datetime

#打开XML文档
xmlpath = os.path.split(os.path.realpath(__file__))[0] #获取当前路径
xmlpath2 = xmlpath.split('src')[0]
dom = xml.dom.minidom.parse(xmlpath2+'testdata\\config.xml')
#得到文档元素对象
root = dom.documentElement

#获取当前时间
now = time.strftime("%Y-%m-%d_%H_%M_%S")
tdata=  time.strftime("%Y-%m-%d")
now_time = datetime.datetime.now()
yes_time = now_time + datetime.timedelta(days=-1)
#昨天的年月日
yes_time_nyr = yes_time.strftime("%Y-%m-%d")


class TestCase_01(test_unittest.TestCase):
    u'''录单任务'''

    @classmethod
    def  setUpClass(cls):#所有用例执行前，执行
        #判断条形码是否获取正确
        if barcode == 0:
            print "条形码获取失败，测试终止！"
            print "请检查条形码生产环境是否正常访问。"
            quit(cls)
        #firefox下载默认设置
        fp = webdriver.FirefoxProfile()
        fp.set_preference("browser.download.folderList",2)
        fp.set_preference("browser.download.manager.showWhenStarting",False)
        fp.set_preference("browser.download.dir", xmlpath2+'log')
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk",
                          "application/octet-stream") #下载文件的类型
        cls.driver = webdriver.Firefox(firefox_profile=fp)
        cls.driver.implicitly_wait(30)
        logins = root.getElementsByTagName('url')
        cls.base_url = logins[0].firstChild.data
        #print self.base_url
        cls.verificationErrors = []
        cls.accept_next_alert = True
    def  setUp(self):#每条用例执行前，执行
        pass
    
    def test_01_login(self):
        u'''登录'''
        driver = self.driver
        driver.get(self.base_url)
        #设置浏览器全屏
        driver.maximize_window()
        logins = root.getElementsByTagName('user')
        #获得user 标签的username、passwrod 属性值
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

            
    def test_02_sllr(self):
        u'''录单任务'''
        driver = self.driver 
        #选择受理-->受理录入
        driver.find_element_by_xpath("/html/body/div[2]/div/div[4]/div/div[6]/div/table/tbody/tr/td[2]/img").click()
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/div[3]/div/div/div/div/table/tbody[2]/tr[3]/td[2]").click()
        #切换到iframe
        driver.switch_to_frame(driver.find_element_by_xpath("/html/body/div[2]/div/div[5]/div/iframe"))
        
        #循环判断该投保单号是否进入任务池中，如果没有，刷新页面。总等待时间5分钟。
        a = 30
        while a>0 :
            
            try:
                driver.find_element_by_link_text(barcode)
                break
            except NoSuchElementException,e:
                time.sleep(10)
                a = a-1
                #返回主frame 
                self.driver.switch_to_default_content()  
                driver.find_element_by_xpath("/html/body/div[2]/div/div[4]/div/div[5]/div/table/tbody/tr/td/table/tbody/tr/td[2]/img").click()
                driver.find_element_by_xpath("/html/body/div[3]/div/div/div/div/table/tbody[2]/tr[3]/td[2]").click()
                #切换到iframe
                driver.switch_to_frame(driver.find_element_by_xpath("/html/body/div[2]/div/div[5]/div/iframe"))
                
        try: 
            #点击进入录单任务页面
            driver.find_element_by_link_text(barcode).click()
        except NoSuchElementException,e:
            print e, " 任务池中没有该任务，请检查后台程序是否有错。"
            driver.quit()
        #关闭影像页面
        driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div').click()
        driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div[1]/div[2]/div').click()
            
        

        

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
        
       # cls.driver.quit()
        pass

if __name__ == "__main__":
    test_unittest.main()
