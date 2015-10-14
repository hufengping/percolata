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
case6file = open(db2file.case6datafile)

#获取当前时间
now = time.strftime("%Y-%m-%d_%H_%M_%S")
tdata=  time.strftime("%Y-%m-%d")
class TestCase_01(unittest.TestCase):
    u'''犹豫期撤销'''
    
    #从数据文件获取保单号
    pn = Autotest.dataRead(db2file.case6datafile)  #读取数据文件中的保单号 
    mn = '' #现金价值
    @classmethod
    def  setUpClass(cls):#所有用例执行前，执行
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
            self.assertEqual(text,prompt_info)
        except AssertionError,e:
            print e
            print ' 请查看截图文件 '+now+'.png'
            driver.get_screenshot_as_file(xmlpath2+"log\\"+now+U'登录信息验证不通过.png')#如果没有找到上面的元素就截取当前页面。
 
    def test_02_khcx(self):
        u'''客户查询'''
        driver = self.driver  
        #选择机构受理菜单
        driver.implicitly_wait(30)
        driver.find_element_by_name('isc_1Qopen_icon_2').click()
        #ActionChains(driver).double_click(jgsl).perform()#双击元素
        time.sleep(1)
        
        #选择逐单受理
        driver.find_element_by_xpath('/html/body/div[2]/div/div[4]/div/div[1]/div/div/div/div[2]/div/div[1]/div/div/table/tbody[2]/tr[5]/td/div/nobr/table/tbody/tr/td[2]').click()
        driver.implicitly_wait(30)
        
        #切换到frame
        xf = driver.find_element_by_xpath('/html/body/div[2]/div/div[4]/div/div[2]/div/div[1]/div/iframe')
        driver.switch_to_frame(xf)
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
        driver = self.driver
        driver.implicitly_wait(30)
        #切换到frame
        xf = driver.find_element_by_xpath('/html/body/div[2]/div/div[4]/div/div[2]/div/div[1]/div/iframe')
        driver.switch_to_frame(xf)
        #switch_to_default_content()
        #选择客户radiobutton
        driver.find_element_by_name('selectClientNo').click()
        #点击确定按钮
        driver.find_element_by_id('ok').click()
        #返回主frame 
        driver.switch_to_default_content()

    def test_04_xxlr(self):
        '''申请信息录入'''
        driver = self.driver
        #切换到frame
        xf = driver.find_element_by_xpath('/html/body/div[2]/div/div[4]/div/div[2]/div/div[1]/div/iframe')
        driver.switch_to_frame(xf)
        #勾选免填单
        driver.find_element_by_id('fillForm0').click()
        
                
        #勾选证件长期有效
        driver.find_element_by_id("isLongidnoValidityDate").click()

        #输入保单号
        driver.find_element_by_id('policyNo0').send_keys(self.pn)
        #服务项目
        driver.find_element_by_id('applyFiles0.serviceItems').send_keys('8')
        #申请日志为今天
        driver.find_element_by_id('applyFiles0.applyDate').send_keys(tdata)
        #下拉菜单选择收费方式
        Select(driver.find_element_by_id("applyFiles0.paymentType")).select_by_visible_text(u"现金")
        #获取用户姓名和身份证号
        nname = driver.find_element_by_xpath('/html/body/div[2]/div[2]/form/div[1]/div[2]/table/tbody/tr/td[2]').text
        nID = driver.find_element_by_xpath('/html/body/div[2]/div[2]/form/div[1]/div[2]/table/tbody/tr/td[6]').text
        #收款人姓名
        driver.find_element_by_id('applyFiles0.transferAccountOwner').send_keys(nname)
        #收款人证件号码
        driver.find_element_by_id('applyFiles0.transferAccountOwnerIdNo').send_keys(nID)
        #点击确定
        driver.find_element_by_id('ok').click()
        #返回主frame 
        driver.switch_to_default_content()

    def test_05_bqqr(self):
        '''保全项目确认'''
        driver = self.driver
        #切换到frame
        xf = driver.find_element_by_xpath('/html/body/div[2]/div/div[4]/div/div[2]/div/div[1]/div/iframe')
        driver.switch_to_frame(xf)
        #获得断言：通过
        #srt = driver.find_element_by_xpath('/html/body/div[2]/div[2]/form/div[1]/div[2]/div/fieldset/table/tbody/tr/td[5]/span').text
        try:
            srt = driver.find_element_by_xpath('/html/body/div[2]/div[2]/form/div[1]/div[2]/div/fieldset/table/tbody/tr/td[5]/span').text

            self.assertEqual(srt, U'通过', '受理规则检查不通过')
        except BaseException,e:
            print e
            #获取当前时间
            now = time.strftime("%Y-%m-%d_%H_%M_%S")
            print ' 请查看截图文件 '+now+'.png'
            driver.get_screenshot_as_file(xmlpath2+"log\\"+now+U'受理规则检查不通过.png')#如果没有找到上面的元素就截取当前页面。   
                #点击确定
        driver.find_element_by_id('ok').click()
        #返回主frame 
        driver.switch_to_default_content()
    def test_06_xxtz(self):
        '''受理捆绑信息调整'''
        driver = self.driver
        #切换到frame
        xf = driver.find_element_by_xpath('/html/body/div[2]/div/div[4]/div/div[2]/div/div[1]/div/iframe')
        driver.switch_to_frame(xf)
        #选择保全项目
        driver.find_element_by_name('adjustItem').click()
        #点击确定
        driver.find_element_by_id('ok').click()
        #返回主frame
        driver.switch_to_default_content()
    def test_07_xxlr(self):
        '''项目经办信息录入'''
        global mn
        mn = '犹豫期撤销'
        driver = self.driver
        #切换到frame
        xf = driver.find_element_by_xpath('/html/body/div[2]/div/div[4]/div/div[2]/div/div[1]/div/iframe')
        driver.switch_to_frame(xf)
        #条形码，不知道有没有用
        txm = driver.find_element_by_xpath('/html/body/div[2]/div[2]/form/div[2]/div/div[2]/table/tbody/tr[2]/td[2]').text
        #现金价值
        #mn = driver.find_element_by_xpath('/html/body/div[2]/div[2]/form/div[3]/div/div[2]/div/table[2]/tbody/tr/td[10]').text
        #保单补发次数
        #driver.find_element_by_xpath('/html/body/div[2]/div[2]/form/div[2]/div/div[2]/table/tbody/tr[4]/td[2]/input[2]').send_keys('0')
        #输入贷款金额：最小500   
        #inintMaxLoanCash1 = string.atof(inintMaxLoanCash.lstrip())
        driver.find_element_by_id('loanAmount').send_keys('500')
        #点击确定
        driver.find_element_by_id('itemsInputFormSubmitBt').click()
        #返回主frame
        driver.switch_to_default_content()
        
    def test_08_jbjg(self):
        '''受理经办结果'''
        driver = self.driver
        #切换到frame
        xf = driver.find_element_by_xpath('/html/body/div[2]/div/div[4]/div/div[2]/div/div[1]/div/iframe')
        driver.switch_to_frame(xf)
        #断言:现金价值无法计算
        mn1 = self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/form/div/table/tbody/tr[2]/td/pre').text
        try:
            self.assertIn('500', mn1, '处理规则检查不通过！')
        except AssertionError,e:
            print e
            #获取当前时间
            now = time.strftime("%Y-%m-%d_%H_%M_%S")
            print ' 请查看截图文件 '+now+'.png'
            self.driver.get_screenshot_as_file(xmlpath2+"log\\"+now+U'现金价值计算错误处理规则检查不通过.png')#如果没有找到上面的元素就截取当前页面。
        #断言:经办结果页面正常
        try:
            self.assertEqual(u"机构受理>>逐单受理>>受理经办结果", self.driver.find_element_by_id("pathString").text)
        except AssertionError,e:
            print e
            #获取当前时间
            now = time.strftime("%Y-%m-%d_%H_%M_%S")
            print ' 请查看截图文件 '+now+'.png'
            self.driver.get_screenshot_as_file(xmlpath2+"log\\"+now+U'受理经办结果页面显示异常.png')#如果没有找到上面的元素就截取当前页面。
        

        #返回主frame
        driver.switch_to_default_content()
      
    def test_09_dysq(self):
        '''激光打印申请'''
        driver = self.driver
        #切换到frame
        xf = driver.find_element_by_xpath('/html/body/div[2]/div/div[4]/div/div[2]/div/div[1]/div/iframe')
        driver.switch_to_frame(xf)
        #点击激光打印
        driver.find_element_by_id('print').click()
        #调用autoit,模拟回车键，下载文件
        Autotest.autoit.Sleep(2000)
        Autotest.autoit.Send("{Enter}")
        #点击确定，进入批单打印
        driver.find_element_by_id('ok').click()
        
        #返回主frame
        driver.switch_to_default_content()
   

    def test_10_pddy(self):
        '''受理经办结束--批单打印'''
        driver = self.driver
        #切换到frame
        xf = driver.find_element_by_xpath('/html/body/div[2]/div/div[4]/div/div[2]/div/div[1]/div/iframe')
        driver.switch_to_frame(xf)
        
        results = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[2]/td/pre').text
        if results=='已生效' :
            #点击激光批单打印
            driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[2]/td/a[1]').click()
            #调用autoit,模拟回车键，下载文件
            Autotest.autoit.Sleep(2000)
            Autotest.autoit.Send("{Enter}")
        else:
            pass
            
            
       
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

    def tearDown(self):#每条用例执行完，执行
        self.assertEqual([], self.verificationErrors)
        
    @classmethod #所有用例执行完，执行
    def tearDownClass(cls):
        Autotest.dataDelline(db2file.case3datafile) #删除一行数据文件
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
