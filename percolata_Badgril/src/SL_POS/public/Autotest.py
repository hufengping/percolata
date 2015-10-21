#coding=utf-8
'''
@author: fengping.hu
'''
import time, os, string, datetime,sys
from email.mime.text import MIMEText
from stat import *
from os import listdir
from os.path import isdir
#email
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import configparser

# cur_file_dir
def cur_file_dir():
    path = sys.path[0]
    if os.path.isdir(path):
         return path
    elif os.path.isfile(path):
         return os.path.dirname(path)

# read credentials
CREDENTIALS_FILE =cur_file_dir() + '/.credentials'
print sys.path[0]
cred = configparser.ConfigParser()
cred.read(CREDENTIALS_FILE)

def newfile(result_dir):
    '''Find the latest file'''
    # Get all the files in the directory
    lists = os.listdir(result_dir)
    # Re arrange the files in the directory by time.
    lists.sort(key=lambda fn: os.path.getmtime(result_dir+"/"+fn))
    print 'Latest log:'+lists[-1]
    FILE = os.path.join(result_dir,lists[-1])
    return FILE


# get time
def getTime(style = '%Y-%m-%d %H:%M:%S'):
    return time.strftime(style, time.localtime())
def mail(mail_to,subject, text):
    """send email"""
    """embed tracking code and mail to all emails
    :rtype : object
    """
    mailserver = smtplib.SMTP("smtp.gmail.com", 587)
    mailserver.starttls()
    mailserver.ehlo()
    mailserver.login(cred.get('GMAIL','USER'), cred['GMAIL']['PASSWD'])

    msg = MIMEMultipart()
    msg['From'] = cred.get('GMAIL','USER')
    msg['Subject'] = subject
    msg.attach(MIMEText(text, 'html'))
    mailserver.sendmail(cred.get('GMAIL','USER'), mail_to, msg.as_string())

    mailserver.close()

'''file cop'''
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
