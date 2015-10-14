#coding=utf-8
'''
Created on 2015年3月18日

@author: fengping.hu
'''

from win32com.client import Dispatch
import time,os
import smtplib
import cx_Oracle
import ConfigParser


inipath1 = os.path.split(os.path.realpath(__file__))[0] #获取当前路径
inipath2 = inipath1.split('src')[0]
#获取ini路径
inipath = inipath2+'testdata\\config.ini' 
#数据文件路径
case1datafile = inipath2+'testdata\\case1.data'
case2datafile = inipath2+'testdata\\case2.data'
case3datafile = inipath2+'testdata\\case3.data'
case4datafile = inipath2+'testdata\\case4.data'
case5datafile = inipath2+'testdata\\case5.data'
case6datafile = inipath2+'testdata\\case6.data'
case7datafile = inipath2+'testdata\\case7.data'

#ini文件载入
config = ConfigParser.ConfigParser()
config.readfp(open(inipath))
#oracle数据库配置
oracle_username = config.get('oracle','username')
oracle_password = config.get('oracle','password')
oracle_database = config.get('oracle','database')
#获取当前月份
tmonth = time.strftime("%Y-%m")

def updataFile():
    nmonth = config.get('data','month')
    if nmonth != tmonth:
        conDatabase_case1()
        conDatabase_case2()
        conDatabase_case3()
        conDatabase_case4()
        conDatabase_case5()
        conDatabase_case6()
        conDatabase_case7()
        print '上次执行月份为： '+nmonth +'更新数据文件……'
        #写入ini
        config.set("data", "month",tmonth)
        config.write(open(inipath, "r+"))
        
    else:
        pass
def conDatabase_case1():
    '''保全项：退保试算'''
    #建立和数据库系统的连接  
    con = cx_Oracle.connect(oracle_username,oracle_password,oracle_database)
    #获取操作游标
    cursor = con.cursor()
    #执行sql语句
    #退费试算  重疾：case1
    cursor.execute("""SELECT ta.policy_no,ta.product_code,tc.full_name
  FROM POLICY_PRODUCT TA, PRODUCT_CLASS TB,product tc
 WHERE TA.DUTY_STATUS = '1'
   AND TA.PRODUCT_CODE = TB.PRODUCT_CODE
   AND TB.CLASS_CODE = '14'
   AND ta.prod_seq = 1
   AND ta.product_code = tc.product_code
   AND TA.effect_date<sysdate-60
   AND rownum<='100'""") 
    #config.add_section("case1")
    #创建数据文件
    case1file = open(case1datafile,'w+')  
    while (1):  
        row = cursor.fetchone()  
        if row == None:  
            break  
        case1file.write(row[0]+'\n') #写入数据文件
    
    case1dataln = cursor.rowcount  #数据文件长度
    case1file.close() 
    #关闭连接，释放资源 
    cursor.close()
    con.close() 
def conDatabase_case2():
    '''保全项：整单退保'''
    #建立和数据库系统的连接  
    con = cx_Oracle.connect(oracle_username,oracle_password,oracle_database)
    #获取操作游标
    cursor = con.cursor()  
    #执行sql语句
    #保全项：保全受理退保保全项；case02
    cursor.execute("""select a.policy_no
  from pos_fin_contract a, policy b
 where a.policy_no = b.policy_no
   and b.duty_status = '1' and b.effect_date<sysdate-60
   AND rownum<='100'""") 

    #创建数据文件
    case2file = open(case2datafile,'w+')  
    while (1):  
        row = cursor.fetchone()  
        if row == None:  
            break  
        case2file.write(row[0]+'\n') #写入数据文件
    
    case2dataln = cursor.rowcount  #数据文件长度
    case2file.close() 
    #关闭连接，释放资源 
    cursor.close()
    con.close() 

def conDatabase_case3():
    '''保全项：附加险退保'''
    #建立和数据库系统的连接  
    con = cx_Oracle.connect(oracle_username,oracle_password,oracle_database)
    #获取操作游标
    cursor = con.cursor()  
    #执行sql语句
    #保全项：附加险单独退保；case03
    cursor.execute("""select * from policy_product a 
where  a.duty_status='2' 
   and a.lapse_reason='8' 
   and a.prod_seq>1
   AND rownum<='100'""") 

    #创建数据文件
    case3file = open(case3datafile,'w+')  
    while (1):  
        row = cursor.fetchone()  
        if row == None:  
            break  
        case3file.write(row[0]+'\n') #写入数据文件
    
    case3dataln = cursor.rowcount  #数据文件长度
    case3file.close() 
    #关闭连接，释放资源 
    cursor.close()
    con.close() 

def conDatabase_case4():
    '''保全项：犹豫期撤销'''
    #建立和数据库系统的连接  
    con = cx_Oracle.connect(oracle_username,oracle_password,oracle_database)
    #获取操作游标
    cursor = con.cursor()  
    #执行sql语句
    #保全项：犹豫期撤销；契撤（整单）；case04
    cursor.execute("""select *
  from policy_product a, policy_contract b
 where a.duty_status = '1'
   and b.policy_no = a.policy_no
   and ((b.provide_date > sysdate - 10 and b.confirm_date is null) or
       (b.confirm_date > sysdate - 10))
   AND rownum<='100'""") 

    #创建数据文件
    case4file = open(case4datafile,'w+')  
    while (1):  
        row = cursor.fetchone()  
        if row == None:  
            break  
        case4file.write(row[0]+'\n') #写入数据文件
    
    case4dataln = cursor.rowcount  #数据文件长度
    case4file.close() 
    #关闭连接，释放资源 
    cursor.close()
    con.close() 

def conDatabase_case5():
    '''保全项：部分领取'''
    #建立和数据库系统的连接  
    con = cx_Oracle.connect(oracle_username,oracle_password,oracle_database)
    #获取操作游标
    cursor = con.cursor()  
    #执行sql语句
    #保全项：部分领取；case05
    cursor.execute("""select a.policy_no
  from pos_fin_contract a, policy b
 where a.policy_no = b.policy_no
   and b.duty_status = '1' and b.effect_date<sysdate-60
   AND rownum<='100'""") 

    #创建数据文件
    case5file = open(case5datafile,'w+')  
    while (1):  
        row = cursor.fetchone()  
        if row == None:  
            break  
        case5file.write(row[0]+'\n') #写入数据文件
    
    case5dataln = cursor.rowcount  #数据文件长度
    case5file.close() 
    #关闭连接，释放资源 
    cursor.close()
    con.close() 

def conDatabase_case6():
    '''保全项：保单贷款'''
    #建立和数据库系统的连接  
    con = cx_Oracle.connect(oracle_username,oracle_password,oracle_database)
    #获取操作游标
    cursor = con.cursor()  
    #执行sql语句
    #保全项：保单贷款；case06
    cursor.execute("""select POLICY_NO
  from policy_product a
 where a.product_code in (select a.product_code
                            from product_parameters a
                           where a.parameter = '400'
                             and a.parameter_value = '1')
   and a.duty_status = '1'
   and a.effect_date < sysdate - 30
   and not exists (select 1
          from policy_suspend_history x
         where x.cancel_time is null
           and x.policy_no = a.policy_no)
   AND rownum<='100'""") 

    #创建数据文件
    case6file = open(case6datafile,'w+')  
    while (1):  
        row = cursor.fetchone()  
        if row == None:  
            break  
        case6file.write(row[0]+'\n') #写入数据文件
    
    case6dataln = cursor.rowcount  #数据文件长度
    case6file.close() 
    #关闭连接，释放资源 
    cursor.close()
    con.close() 


def conDatabase_case7():
    '''保全项：生存金领取'''
    #建立和数据库系统的连接  
    con = cx_Oracle.connect(oracle_username,oracle_password,oracle_database)
    #获取操作游标
    cursor = con.cursor()  
    #执行sql语句
    #保全项：生存金领取；case07
    cursor.execute("""select POLICY_NO 
  from pos_survival_due p
 where p.valid_flag = 'Y'
   and p.pay_due_flag = 'Y'
  and p.pay_fact_flag='N'
   AND rownum<='100'""") 

    #创建数据文件
    case7file = open(case7datafile,'w+')  
    while (1):  
        row = cursor.fetchone()  
        if row == None:  
            break  
        case7file.write(row[0]+'\n') #写入数据文件
    
    case7dataln = cursor.rowcount  #数据文件长度
    case7file.close() 
    #关闭连接，释放资源 
    cursor.close()
    con.close() 


if __name__ == '__main__':
    updataFile()