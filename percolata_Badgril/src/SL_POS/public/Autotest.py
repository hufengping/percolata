#coding=utf-8
'''
@author: fengping.hu
'''
import time, os, smtplib, string, datetime
from email.mime.text import MIMEText
from email.header import Header
from stat import *
from os import listdir
from os.path import isdir


import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import configparser


# read credentials
CREDENTIALS_FILE = '.credentials'
cred = configparser.ConfigParser()
cred.read(CREDENTIALS_FILE)

GMAIL_USER = cred['GMAIL']['USER']
GMAIL_PASSWD = cred['GMAIL']['PASSWD']

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

def mail(mail_to,subject, text):
    """embed tracking code and mail to all emails"""
    mailServer =smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(GMAIL_USER, GMAIL_PASSWD)

    msg = MIMEMultipart()
    msg['From'] = GMAIL_USER
    msg['Subject'] = subject
    msg.attach(MIMEText(text, 'html'))
    mailServer.sendmail(GMAIL_USER, mail_to, msg.as_string())

    mailServer.close()

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

    mail("fengping.hu@percolata.com","test","test")
