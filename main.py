# @Albert Wu,Tsinghua University,Oct 30,2020
# booking gymnasium fields 
import requests
import sys
import io
import datetime
import schedule
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from data import gymnasium_id,item_id
import pandas as pd
#booking对应的单列id.csv
id_csv = pd.read_csv('id.csv',usecols=['id'],encoding='gbk')
id_arr = id_csv.values[0:,0]
#booking_2对应的两列id2.csv
id2_csv = pd.read_csv('id2.csv',usecols=['id1','id2'],encoding='gbk')

phone_number=" "#替换为你的号码
user_name = " "#10位数学号，而不是xxx20,yy19等代号
password = " "
gym_name ='气膜馆' 
gym_id = gymnasium_id[gym_name] 
it_id = item_id[gym_name]
date = "2020-11-13"#日期，按照xxxx-xx-xx格式提交
id2_arr = id2_csv.values
############initial parameters##############################
###########END initial parameters##########################
session = requests.Session()
#!!!!!! login_gym()及booking()两个函数请勿进行任何改动！#################
def login_gym():
    
    headers = {
    'Host': '50.tsinghua.edu.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Content-Length': '42',
    'Origin': 'http://50.tsinghua.edu.cn',
    'Connection': 'keep-alive',
    'Referer': 'http://50.tsinghua.edu.cn/userOperation.do?ms=gotoLoginPage',
    'Upgrade-Insecure-Requests': '1'}

    #session = requests.Session()

    login_url = 'http://50.tsinghua.edu.cn/j_spring_security_check'
    login_post_data = {
    'un':user_name,
    'pw':password, 
    'x':'58',
    'y':'15'  
    }
    resp_AccountSave = session.post(login_url, login_post_data,headers=headers)
    print(resp_AccountSave.status_code)
    ######################END login##############################################
    
def booking():
    ######################booking################################################
    def submit_order(id_gym):
        url = 'http://50.tsinghua.edu.cn/gymbook/gymbook/gymBookAction.do?ms=saveGymBook'
        Air_film_gym_book_data = {
            'bookData.totalCost':" ",
            'bookData.book_person_zjh':" ",
            'bookData.book_person_name':" ",
            'bookData.book_person_phone':	phone_number,
            'gymnasium_idForCache':	str(gym_id),
            'item_idForCache':	str(it_id),
            'time_dateForCache':date,

            'userTypeNumForCache':	"1",
            'putongRes':	"putongRes",
            'selectedPayWay':	"1",
            'allFieldTime':	id_gym+"#"+date
        }

        headers_book = {
        'Host': '50.tsinghua.edu.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '42',
        'Origin': 'http://50.tsinghua.edu.cn',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'}
        bad = session.post(url,data=Air_film_gym_book_data,headers=headers_book)
        print(bad.json()['msg']+"1")
        return bad.json()['msg']
    def save_xnjsd(id_field):
        #在预约成功后发起需要校内结算单的请求
        ulr_xnjsd = "http://50.tsinghua.edu.cn/pay/payAction.do?ms=saveXnjsd"
        headers_xnjsd = {
        'Host': '50.tsinghua.edu.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '183',
        'Origin': 'http://50.tsinghua.edu.cn',
        'Referer': 'http://50.tsinghua.edu.cn/gymbook/gymBookAction.do?ms=viewGymBook&gymnasium_id='+str(gym_id)+'&item_id='+str(it_id)+'&time_date='+date+'&userType=',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'}
        #xm:对应为姓名中文的十六进制编码，此处默认为吴林峰
        #校内结算单似乎无论选择要或是不要都可以现场开具，姓名及院系也可以任意指定
        xnjsd_data = {
            'xm':"%CE%E2%C1%D6%B7%E5",
            'dept':"%B9%A4%CE%EF%CF%B5",
            'gymnasium_idForCache':str(gym_id),
            'item_idForCache':str(it_id),
            'time_dateForCache':date,
            'userTypeNumForCache':"1",
            'allFieldTime':id_field+"#"+date


        }
        xnjsd = session.post(ulr_xnjsd,xnjsd_data,headers=headers_xnjsd)
        print(xnjsd.status_code)
    for id_index in id_arr:
        if submit_order(str(id_index))=="预定成功" :
            save_xnjsd(str(id_index))
            print("请于15分钟内登陆平台支付，否则会自动取消")
            break
##################END booking#################################################
def booking_2():
    ###booking_2()以list形式可以同时提交两个场地或者是一个场地的两个小时，只要提交两个id即可###############
    ######################booking################################################
    def submit_order(id_gym_1,id_gym_2):
        url = 'http://50.tsinghua.edu.cn/gymbook/gymbook/gymBookAction.do?ms=saveGymBook'
        Air_film_gym_book_data = {
            'bookData.totalCost':" ",
            'bookData.book_person_zjh':" ",
            'bookData.book_person_name':" ",
            'bookData.book_person_phone':	phone_number,
            'gymnasium_idForCache':	str(gym_id),
            'item_idForCache':	str(it_id),
            'time_dateForCache':date,

            'userTypeNumForCache':	"1",
            'putongRes':	"putongRes",
            'selectedPayWay':	"1",
            'allFieldTime':	[id_gym_1+"#"+date,id_gym_2+"#"+date]
        }

        headers_book = {
        'Host': '50.tsinghua.edu.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '42',
        'Origin': 'http://50.tsinghua.edu.cn',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'}
        bad = session.post(url,data=Air_film_gym_book_data,headers=headers_book)
        print(bad.json()['msg']+"2")
        return bad.json()['msg']
    def save_xnjsd(id_gym_1,id_gym_2):
        #在预约成功后发起需要校内结算单的请求
        ulr_xnjsd = "http://50.tsinghua.edu.cn/pay/payAction.do?ms=saveXnjsd"
        headers_xnjsd = {
        'Host': '50.tsinghua.edu.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '183',
        'Origin': 'http://50.tsinghua.edu.cn',
        'Referer': 'http://50.tsinghua.edu.cn/gymbook/gymBookAction.do?ms=viewGymBook&gymnasium_id='+str(gym_id)+'&item_id='+str(it_id)+'&time_date='+date+'&userType=',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'}
        #xm:对应为姓名中文的十六进制编码
        xnjsd_data = {
            'xm':"%CE%E2%C1%D6%B7%E5",
            'dept':"%B9%A4%CE%EF%CF%B5",
            'gymnasium_idForCache':str(gym_id),
            'item_idForCache':str(it_id),
            'time_dateForCache':date,
            'userTypeNumForCache':"1",
            'allFieldTime':[id_gym_1+"#"+date,id_gym_2+"#"+date]


        }
        xnjsd = session.post(ulr_xnjsd,xnjsd_data,headers=headers_xnjsd)
        #print(xnjsd.status_code)
        print("校内结算单···")
    
    for id_1,id_2 in id2_arr:
        if submit_order(str(id_1),str(id_2))=="预定成功" :
            save_xnjsd(str(id_1),str(id_2))
            print("请于15分钟内登陆平台支付，否则会自动取消")
            break
##################END booking_2#################################################

##################start schedule##############################################
scheduler = BlockingScheduler()
#此处第一个add_job设置时间比预定时间早一分钟，因为login_gym函数为登陆函数，需要花费一定时间
#第二个函数booking为预订场地函数
#以下两行设置的为早上八点开始预订场地，如无其他要求，也无需改动
scheduler.add_job(login_gym, 'cron', day_of_week='*', hour=7, minute=59)
#同时只预约一个场地的一个时段采用下面一行
scheduler.add_job(booking_2, 'cron', day_of_week='*', hour=8, minute=0)
scheduler.add_job(booking, 'cron', day_of_week='*', hour=8, minute=0)
#同时需要预约两个场地或者一个场地的两个时段请注释掉上一行，取消下一行的注释
#当然也可以同时运行booking()和booking_2()，两个线程
#scheduler.add_job(booking_2, 'cron', day_of_week='*', hour=8, minute=0)
scheduler.start()
####################END schedule##############################################
