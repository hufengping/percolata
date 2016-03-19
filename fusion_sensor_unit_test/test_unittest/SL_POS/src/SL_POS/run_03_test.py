#coding=utf-8
import test_unittest
import HTMLTestRunner #引入HTMLTestRunner
import time,os,sys
from public import Autotest
from public import db2file
import ConfigParser

#定义搜索testcase的方法，返回testsuite
def creatsuite():
    testunit = test_unittest.TestSuite()
    #定义测试文件查找的目录
    test_dir= xmlpath
    #定义discover 方法的参数
    discover=test_unittest.defaultTestLoader.discover(test_dir,
                                                 pattern ='testsuite_03.py',
                                                 top_level_dir=None)
    #discover 方法筛选出来的用例，循环添加到测试套件中
    for test_suite in discover:
        for test_cases in test_suite:
            testunit.addTest(test_cases)
            print testunit
    return testunit
#获取当前时间
now = time.strftime("%Y-%m-%d_%H_%M_%S")
#定义报告存放地点
xmlpath = os.path.split(os.path.realpath(__file__))[0] #获取当前路径
xmlpath2 = xmlpath.split('src')[0]
filename = xmlpath2+'log\\'+now+'result.html'
source1 = xmlpath2+r"log" 
target_dir1 = "D:\\jenkins\\workspace\\POS_003"
#获取ini路径
inipath = xmlpath2+'testdata\\config.ini' 
#ini文件载入
config = ConfigParser.ConfigParser()
config.readfp(open(inipath))
mail_from = config.get('mail','from')
mail_to = config.get('mail', 'to')


fp = file(filename, 'wb')
runner =HTMLTestRunner.HTMLTestRunner(
                                      stream=fp,
                                      title=u'个险保全系统测试报告',
                                      description=u'用例执行情况：')
if __name__ == '__main__':
    #检查数据文件是否需要更新
    db2file.updataFile()
    alltestnames = creatsuite()
    runner.run(alltestnames)
    fp.close()
    reportname = Autotest.newfile(xmlpath2+'log\\')
    Autotest.sendMail(mail_from,mail_to, '核心系统自动化运行结果', reportname)   
    Autotest.copynewfiles(source1,target_dir1)