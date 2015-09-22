#coding=utf-8

import win32api, win32pdhutil, win32con,sys 
import win32com.client
from win32com.client import Dispatch
import time,os
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import cx_Oracle

#登录
def login(self,username,password):
    driver = self.driver
    driver.find_element_by_id("j_username").clear()
    driver.find_element_by_id("j_username").send_keys(username)
    driver.find_element_by_id("j_password").clear()
    driver.find_element_by_id("j_password").send_keys(password)
    driver.find_element_by_link_text('登 录').click()
#退出
def logout(self):
    driver = self.driver
    driver.find_element_by_link_text(u"退出").click()
    
############################调用autoit3##########################
try:
    autoit = Dispatch("AutoItX3.Control")
except:
    print >> sys.stderr, u'AutoItX3 加载失败了！'

#############################查找最新文件##########################    
def newfile(result_dir):
    #定义文件目录
    #result_dir = 'D:\\Workspaces\\python\\TestLogin126\\log'
    #获取目录下所有文件
    lists=os.listdir(result_dir)
    #重新按时间对目录下的文件进行排列
    lists.sort(key=lambda fn: os.path.getmtime(result_dir+"\\"+fn))
    print ('最新日志： '+lists[-1])
    file = os.path.join(result_dir,lists[-1])
    #print file
    return file
############################发送邮件##########################
#获取当前时间戳
def getTime(style = '%Y-%m-%d %H:%M:%S'):
    return time.strftime(style, time.localtime())

def sendMail(mail_from, mail_to, mail_title, mail_content, mail_server=r'szhubap.sino-life.com', mail_port=25):
    try:
        handle = smtplib.SMTP(mail_server, mail_port)
        #handle = smtplib.SMTP('mail.360.cn', 25)
        handle.ehlo()  
        handle.starttls()  
        handle.ehlo()  
        mail_data = getTime()
        
        #定义正文
        f = open(mail_content, 'rb')
        mail_body = f.read()
        f.close()
        
        msg = "From: %s\r\nTo: %s\r\nData: %s\r\nContent-Type: text/html;charset=gb2312\r\nSubject: %s \r\n\r\n %s\r\n"  % (mail_from, str(mail_to).replace('[', '').replace(']', ''), mail_data, mail_title, mail_body)
        print msg
        handle.sendmail('%s' % mail_from, mail_to, msg)
        handle.close()
    except Exception, e:
        print('sendMail: '+str(e))
        print '发信失败,程序退出...'
        
        
###########################链接数据库############################   
def conDatabase():
    con = cx_Oracle.connect( "ovsee", "life12345","INT2")
    cursor = con.cursor()
    print cursor
    cursor.close()
    con.close() 
if __name__ == '__main__':
    autoit.MouseMove(100, 100)
    sendMail('badgirl@sino-life.com',['fengping.hu@sino-life.com'], '核心系统自动化运行结果', 'D:\\Workspaces\\python\\TestLogin126\\log\\2015-03-11 15_00_07result.html')
    conDatabase()