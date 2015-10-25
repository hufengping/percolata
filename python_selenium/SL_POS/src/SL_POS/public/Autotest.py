#coding=utf-8
'''
Created on 2015年2月8日

@author: fengping.hu
'''
import win32api, win32pdhutil, win32con,sys
import win32com.client
from win32com.client import Dispatch
import time,os,smtplib,string,datetime
from email.mime.text import MIMEText
from email.header import Header
import cx_Oracle
#from public import db2file
import db2file
from stat import *
from os import listdir
from os.path import isdir


#登录
def login(self,username,password):
    driver = self.driver
    driver.find_element_by_id("j_username").clear()
    driver.find_element_by_id("j_username").send_keys(username)
    driver.find_element_by_id("j_password").clear()
    driver.find_element_by_id("j_password").send_keys(password)
    driver.find_element_by_xpath("/html/body/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td[1]/table[2]/tbody/tr[1]/td[4]/input").click()
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
        #print msg
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
###########################读写数据文件############################
#写入数据文件
def dataWrite(filepath,str):
    
    casefile = open(filepath,'w+')
    casefile.write(str+'\n')
    casefile.close()

#读取数据文件首行    
def dataRead(filepath1):
    casefile1 = open(filepath1,'r')
    return casefile1.readline()
    casefile1.close()

#删除数据文件首行后重新写入
def dataDelline(filepath2):
    casefile2=open(filepath2) 
    a=casefile2.readlines() 
    fout=open(filepath2,'w') 
    b=''.join(a[1:]) 
    fout.write(b) 
    casefile2.close() 
    fout.close()  
###########################文件拷贝############################
'''拷贝文件中修改日期为days天内的文件到指定目录'''
def copynewfiles(source,target_dir,dayss=1):
    if isdir(source) != True:
        print 'Error: source is not a directory'
        exit()
    filelist = listdir(source)
    for name in filelist :
        strr = source+"\\"+name
        trrr = target_dir+"\\"+name
        t1 = time.gmtime(os.stat(strr)[ST_MTIME]) #get file's mofidy time
        t11 = time.strftime('%Y-%m-%d',t1)
        year,month,day=t11.split('-')
        t111= datetime.datetime(int(year),int(month),int(day))
        t2 = time.gmtime()
        t22 = time.strftime('%Y-%m-%d',t2)
        year,month,day=t22.split('-')
        t222= datetime.datetime(int(year),int(month),int(day))
        days = (t222-t111).days
        if days < string.atof(dayss) :
            os.system("copy %s %s" % (strr, trrr.strip()))

    
    
    
    
if __name__ == '__main__':
    autoit.MouseMove(100, 100)
    #sendMail('badgirl@sino-life.com',['fengping.hu@sino-life.com'], '核心系统自动化运行结果', 'D:\\Workspaces\\python\\TestLogin126\\log\\2015-03-11 15_00_07result.html')
    #conDatabase()
    #print dataRead(db2file.case1datafile)
    #dataDelline(db2file.case1datafile)
    
    inipath1 = os.path.split(os.path.realpath(__file__))[0] #获取当前路径
    inipath2 = inipath1.split('src')[0]
    print inipath2
    source1 = inipath2+r"log" 
    target_dir1 = inipath2+r"new"
    
    copynewfiles(source1,target_dir1,2)