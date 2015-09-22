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

#创建数据文件
case1file = open(db2file.case1datafile)

#获取当前时间
now = time.strftime("%Y-%m-%d_%H_%M_%S")
tdata=  time.strftime("%Y-%m-%d")
class TestCase_01(unittest.TestCase):
    u'''退保试算'''
    #从数据文件获取保单号
    pn = Autotest.dataRead(db2file.case1datafile)  #读取数据文件中的保单号 
    mn = ''   #存储现金价值
    
    @classmethod
    def  setUpClass(cls):#所有用例执行前，执行
        cls.driver = webdriver.Firefox()
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
            self.assertEqual(text,prompt_info,'登录信息验证不通过，请检查网络或登录信息！')
        except AssertionError,e:
            print e
            print ' 请查看截图文件 '+now+'.png'
            driver.get_screenshot_as_file(xmlpath2+"log\\"+now+U'登录信息验证不通过.png')#如果没有找到上面的元素就截取当前页面。
            return
    def test_02_khcx(self):
        '''客户查询'''
        #选择机构受理菜单
        self.driver.implicitly_wait(30)
        self.driver.find_element_by_name('isc_1Qopen_icon_2').click()
        #ActionChains(driver).double_click(jgsl).perform()#双击元素
        time.sleep(1)
        
        #选择保全试算
        self.driver.find_element_by_xpath('/html/body/div[2]/div/div[4]/div/div[1]/div/div/div/div[2]/div/div/div/div/table/tbody[2]/tr[7]/td').click()
        self.driver.implicitly_wait(30)
        
        #切换到frame
        xf = self.driver.find_element_by_xpath('/html/body/div[2]/div/div[4]/div/div[2]/div/div[1]/div/iframe')
        self.driver.switch_to_frame(xf)
        #switch_to_default_content()
                
        #输入保单号点击查询
        self.driver.find_element_by_name('policyNo').send_keys(self.pn)
        #选择投保人radioButton
        self.driver.find_element_by_id('applicantOrInsured1').click()
        #点击查询
        self.driver.find_element_by_id('search').click()
        #返回主frame 
        self.driver.switch_to_default_content()
    def test_03_khxz(self):
        '''客户选择'''
        self.driver.implicitly_wait(30)
        #切换到frame
        xf = self.driver.find_element_by_xpath('/html/body/div[2]/div/div[4]/div/div[2]/div/div[1]/div/iframe')
        self.driver.switch_to_frame(xf)
        #switch_to_default_content()
        #选择客户radiobutton
        self.driver.find_element_by_name('selectClientNo').click()
        #填入保单号
        self.driver.find_element_by_name('policyNo').send_keys(self.pn)
        #申请日期为今天
        self.driver.find_element_by_name('applyDate').send_keys(tdata)
        #下拉菜单选择退保
        select = self.driver.find_element_by_name('serviceItems')
        select.find_element_by_xpath("//option[@value='2']").click()
        #点击确定按钮
        self.driver.find_element_by_id('ok').click()
        #返回主frame 
        self.driver.switch_to_default_content()
    def test_04_jblr(self):  
        '''项目经办信息录入'''  
        global mn
        self.driver.implicitly_wait(30)
        #切换到frame
        xf = self.driver.find_element_by_xpath('/html/body/div[2]/div/div[4]/div/div[2]/div/div[1]/div/iframe')
        self.driver.switch_to_frame(xf)
        #switch_to_default_content()
        #勾选险种
        self.driver.find_element_by_name('productCb0').click()
        #保存现金价值
        mn = self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/form/div[1]/div/div[2]/div/table/tbody/tr/td[10]').text
        #点击确定
        self.driver.find_element_by_id('itemsInputFormSubmitBt').click()
        #返回frame
        self.driver.switch_to_default_content()
    def test_05_dbjg(self):  
        '''受理经办结果'''  
        self.driver.implicitly_wait(30)
        #切换到frame
        xf = self.driver.find_element_by_xpath('/html/body/div[2]/div/div[4]/div/div[2]/div/div[1]/div/iframe')
        self.driver.switch_to_frame(xf)
        #self.driver.switch_to_default_content()
        #断言:现金价值试算正确
        mn1 = self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/form/div/table/tbody/tr[2]/td/pre').text
        try:
            self.assertIn(mn, mn1, U'现金价值计算错误！')
        except AssertionError,e:
            print e
            #获取当前时间
            now = time.strftime("%Y-%m-%d_%H_%M_%S")
            print u' 请查看截图文件 '+now+'.png'
            self.driver.get_screenshot_as_file(xmlpath2+"log\\"+now+U'现金价值计算错误.png')#如果没有找到上面的元素就截取当前页面。
        #断言:经办结果页面正常
        try:
            self.assertEqual(u"机构受理>>试算>>受理经办结果", self.driver.find_element_by_id("pathString").text,u'受理经办结果页面不正确！')
        except AssertionError,e:
            print e
            #获取当前时间
            now = time.strftime("%Y-%m-%d_%H_%M_%S")
            print ' 请查看截图文件 '+now+'.png'
            self.driver.get_screenshot_as_file(xmlpath2+"log\\"+now+U'受理经办结果页面显示异常.png')#如果没有找到上面的元素就截取当前页面。

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
        Autotest.dataDelline(db2file.case1datafile) #删除一行数据文件
        cls.driver.quit()
        
if __name__ == "__main__":
    unittest.main()
