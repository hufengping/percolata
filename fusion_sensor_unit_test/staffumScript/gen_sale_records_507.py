#!/usr/bin/python
#!coding: utf-8

import requests
import json
import random
import arrow

onlinetoken = "eyJ1c2VybmFtZSI6ImFkbWluQGZpc3Npb25sYWJzLmluIiwicGFzc3dvcmQiOiIkMmEkMTAkTUJMWjdXZlZZT1VGdG0vN2taN1FSdUFRZDhBRUFDcTIuSXZoWjM5VmNsdTJ6alVZemFMUmkiLCJuYW1lIjoiRG9uYWxkIFBsaW5lciIsImlzRW5hYmxlZCI6dHJ1ZSwiaXNEZWxldGVkIjpmYWxzZSwiaXNBY2NvdW50RXhwaXJlZCI6ZmFsc2UsImlzQWNjb3VudExvY2tlZCI6ZmFsc2UsImlzQ3JlZGVudGlhbHNFeHBpcmVkIjpmYWxzZSwibG9jYXRpb25TaGFyaW5nQWxsb3dlZCI6ZmFsc2UsImdvb2dsZUlkIjpudWxsLCJmYklkIjpudWxsLCJsaW5rZWRpbklkIjpudWxsLCJzdG9yZSI6eyJzdG9yZUlkIjo4NCwibmFtZSI6IkRvbmFsZCBQbGluZXIgLSBTYW4gSm9zZSIsImlzRW5hYmxlZCI6dHJ1ZSwiaXNEZWxldGVkIjpmYWxzZSwiZmVhdHVyZUlzRHdzRW5hYmxlZCI6ZmFsc2UsInN0b3JlSG91cnMiOiIxNi01LDE2LTUsMTYtNSwxNi01LDE2LTUsMTYtNSwxNy0yIiwiY2FsZW5kYXJBY2NvdW50IjoiZG9uYWxkLnBsaW5lckBjYWxlbmRhci5wZXJjb2xhdGEuY29tIiwiYXV0b1NjaGVkdWxlQ2FsZW5kYXIiOiJleWVzdGFsa3MuY29tXzNmaHRtcTkwamhwYW0wOWczbmR0ZjU0azdzQGdyb3VwLmNhbGVuZGFyLmdvb2dsZS5jb20iLCJibGFja091dENhbGVuZGFyIjoiZXllc3RhbGtzLmNvbV82am9qMTgwbzNiamszMnN2ODBnOW01c2R1NEBncm91cC5jYWxlbmRhci5nb29nbGUuY29tIiwicmVxdWVzdENhbGVuZGFyIjoiZXllc3RhbGtzLmNvbV9jM2xzMmNjanFnZ3Y3cG52NzZrZ3VkcTVpc0Bncm91cC5jYWxlbmRhci5nb29nbGUuY29tIiwiaHJNYWlsIjpudWxsLCJmaWxlVW5kZXJQcm9jZXNzIjpmYWxzZX0sImNvcnBvcmF0ZXMiOm51bGwsImF1dGhvcml0aWVzIjpbeyJpZCI6MSwiYXV0aG9yaXR5IjoiU1RBRkZVTV9BRE1JTklTVFJBVE9SIn1dLCJleHBpcmVzIjoxNTc3ODM2ODAwMDAwLCJzYWxhcnkiOm51bGwsInByb2R1Y3Rpdml0eSI6bnVsbCwicGhvbmVOdW1iZXIiOm51bGwsInR1dG9yaWFsU3RhdHVzIjpudWxsfQ==.ebQV2XA+H7e3obEHyme7zkQMy+B4DmQxJgBB+TbUvvg="
onlineheaders = {'x-auth-token':onlinetoken,'content-type': 'application/json'}

name = ['Jimmy Choo','Jose Hernandez','Zuleeka Mohammed','Varun Senthilkumar','Shaun Benjamin','Shaun Kaeffer','Sammy Sanchez','Pingan','Patrick Cho','Matthew Mountford','Lucy Nyugen','Anielka Mendez','Zhiwei Yang','gaolei','Kevin Minions','Kate Spade','Garrett wong','Janice Franzino','Hanna Smith','Andre Lismonde']

email =['jim@gmail.com','loli@gmail.com','zuleeka@calendar.percolata.com','varun@calendar.percolata.com','surabhi.ramachandra@calendar.percolata.com','shaun@calendar.percolata.com','sammy@calendar.percolata.com','riche.zhang@percolata.com','patrick@calendar.percolata.com','matthew@calendar.percolata.com','lucy@gmail.com','anielka@calendar.percolata.com','lily@gmail.com','lei.gao@percolata.com','kevin@gmail.com','kate@gmail.com','garrett@calendar.percolata.com','jan@calendar.percolata.com','fishman@gmail.com','andre@calendar.percolata.com']

date = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30']  #if the month has 31, add it manually


def insert_sales_records():
    month = raw_input("")
    for i in date:
        getdailyurl="http://104.197.70.18/api/v1/calendar/slots/daily?from=2015-%s-%sT08:00:00-07:00&to=2015-%s-%sT23:00:00-07:00&storeid=507&username=" %(month,i,month,i)
        schedule = requests.get(getdailyurl,headers=onlineheaders)
        dto = schedule.content
        j = json.loads(dto)
        l = j['result']
        if len(l) !=0:
            for _id,d in enumerate(l):
                t = l[_id]['type']
                if t == "SCHEDULE":
                    ename=d['owner']['name']
                    f=d['from']
                    t=d['to']
                    fromday = arrow.get(f).to('utc').replace(hours=1).format()
                    today = arrow.get(t).to('utc').replace(hours=-1).format()
                    #xrandom = random.randint(10,19)
                    mm = random.randint(10,59)
                    price = random.randint(50,500)
                    dot=random.randint(1,9)
                    print "INSERT INTO `store_sales_records` (`location_id`,`time`,`sales_rep`,`item`,`description`,`price`,`quantity`,`extended`,`commission`,`updated_at`) VALUES (507,'%s','%s','Nourishing Oil Cleanser %s ml','Nourishing Oil Cleanser %s ml',%s.%s,1,%s.%s,0,'%s');" % (fromday,ename,mm,mm,price,dot,price,dot,today)

if __name__ == '__main__':
    insert_sales_records()