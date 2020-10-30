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

id_csv = pd.read_csv('id.csv',usecols=['id'],encoding='gbk')
id_arr = id_csv.values[0:,0]
############initial parameters##############################
phone_number=" "
user_name = " "#10位数学号，而不是xxx20,yy19等代号
password = " "
gym_name ='气膜馆' 
gym_id = gymnasium_id[gym_name] 
it_id = item_id[gym_name]
date = "2020-11-02"
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
        print(bad.json()['msg'])
        return bad.json()['msg']

    for id_index in id_arr:
        if submit_order(str(id_index))=="预定成功" :
            break
##################END booking#################################################

##################start schedule##############################################
scheduler = BlockingScheduler()
#此处第一个add_job设置时间比预定时间早一分钟，因为该函数为登陆函数，需要花费一定时间
#第二个函数为预订场地函数
#如果计划早上八点开始预订，则取消以下两行的注释，并注释掉倒数2、3两行
# scheduler.add_job(login_gym, 'cron', day_of_week='*', hour=7, minute=59)
# scheduler.add_job(booking, 'cron', day_of_week='*', hour=8, minute=0)
scheduler.add_job(login_gym, 'cron', day_of_week='*', hour=19, minute=1)
scheduler.add_job(booking, 'cron', day_of_week='*', hour=19, minute=2)
scheduler.start()
####################END schedule##############################################
