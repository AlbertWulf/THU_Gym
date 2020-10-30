import json
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
#仅为羽毛球部分
gymnasium_id = {
    '气膜馆':'3998000',
    '西体育馆':'4836273'
}
item_id = {
    '气膜馆':'4045681',
    '西体育馆':'4836196'
}
