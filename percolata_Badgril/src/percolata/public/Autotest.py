#coding=utf-8
'''
@author: fengping.hu
'''
import time, os, string, datetime,sys
from stat import *
from os import listdir
from os.path import isdir
#email
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase.MIMEBase import MIMEText
from email.mime.text import MIMEText
import configparser

# read credentials
CREDENTIALS_FILE =os.path.split(__file__)[0] + '/.credentials'
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
    mailserver = smtplib.SMTP("smtp.gmail.com", 587)
    mailserver.starttls()
    mailserver.ehlo()
    mailserver.login(cred.get('GMAIL','USER'), cred['GMAIL']['PASSWD'])

    msg = MIMEText(text,'html','utf-8')
    #msg['From'] = cred.get('GMAIL','USER')
    msg['From'] = "badgril@percolata.com"
    msg['Subject'] = subject
    mailserver.sendmail(cred.get('GMAIL','USER'), mail_to, msg.as_string())
    mailserver.close()


def sendMail(mail_from, mail_to, mail_title, mail_content, mail_server=r'smtp.gmail.com', mail_port=587):
    try:
        handle = smtplib.SMTP(mail_server, mail_port)
        #handle = smtplib.SMTP('mail.360.cn', 25)
        handle.ehlo()
        handle.starttls()
        handle.ehlo()
        handle.starttls()
        handle.login(cred.get('GMAIL','USER'), cred['GMAIL']['PASSWD'])
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




def copynewfiles(source,target_dir,dayss=1):
    '''file copy'''
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
