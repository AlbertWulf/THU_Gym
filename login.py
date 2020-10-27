import requests
import sys
import io
import datetime
import schedule
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from data import gymnasium_id,item_id
username =input("pls input ur student's number:")
password =input("pls input ur password:")
book_date = input('pls input date(format example:2020-10-28):')
gym = input('pls input name of the gymnasium:[气膜馆,西体育馆]:')
place_id = input('pls input place id:')

def book_pingpang(username,password,book_date,gym,place_id):
    ###############login##################
    
    headers = {
    'Host': '50.tsinghua.edu.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Content-Length': '42',
    'Origin': 'http://50.tsinghua.edu.cn',
    'Connection': 'keep-alive',
    'Referer': 'http://50.tsinghua.edu.cn/userOperation.do?ms=gotoLoginPage',
    'Upgrade-Insecure-Requests': '1'}

    session = requests.Session()

    login_url = 'http://50.tsinghua.edu.cn/j_spring_security_check'
    login_post_data = {
    'un':str(username),
    'pw':str(password), 
    'x':'58',
    'y':'15'  
    }
    resp_AccountSave = session.post(login_url, login_post_data,headers=headers)
    print(resp_AccountSave.status_code)
    ######################END login##############################################
    
    #################################get id for places###########################

    ######################booking################################################
    url = 'http://50.tsinghua.edu.cn/gymbook/gymbook/gymBookAction.do?ms=saveGymBook'
    Air_film_gym_book_data = {
        'bookData.totalCost':" ",
        'bookData.book_person_zjh':" ",
        'bookData.book_person_name':" ",
        'bookData.book_person_phone':	"18800136325",
        'gymnasium_idForCache':	gymnasium_id[gym],
        'item_idForCache':	item_id[gym],
        'time_dateForCache':str(book_date),
        'userTypeNumForCache':	"1",
        'putongRes':	"putongRes",
        'selectedPayWay':	"1",
        'allFieldTime':	str(place_id)+"#"+str(book_date)
    }
    # West_Gymnasium_book_data = {
    #     'bookData.totalCost':" ",
    #     'bookData.book_person_zjh':" ",
    #     'bookData.book_person_name':" ",
    #     'bookData.book_person_phone':	"18800136325",
    #     'gymnasium_idForCache':	"4836273",
    #     'item_idForCache':	"4836196",
    #     'time_dateForCache':"2020-10-28",
    #     'userTypeNumForCache':	"1",
    #     'putongRes':	"putongRes",
    #     'selectedPayWay':	"1",
    #     'allFieldTime':	"4046188#2020-10-28"
    # }
    headers_book = {
    'Host': '50.tsinghua.edu.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Content-Length': '42',
    'Origin': 'http://50.tsinghua.edu.cn',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'}
    bad = session.post(url,data=Air_film_gym_book_data,headers=headers_book)
    print(bad.json())
hour = input("pls input hour:(24h):")
minute = input("pls input minute:")
scheduler = BlockingScheduler()
scheduler.add_job(book_pingpang(username,password,book_date,gym,place_id), 'cron', day_of_week='*', hour=hour, minute=minute)
scheduler.start()

