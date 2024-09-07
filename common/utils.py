import numpy as np
from datetime import datetime, timedelta
# 类型转换方法
def to_date(str):
    return datetime.strptime(str, "%Y-%m-%d").date()

def to_percent_str(percent, dot=2):
    return format(percent * 100, f'.{dot}f')+"%"

def round(num, dot=2):
    return np.round(num, dot)

def gen_date_pair(end_date, num_of_days):
    start_date = end_date - timedelta(days=num_of_days)
    return start_date, end_date
def gen_date_list(end_date, num_of_days):
    li = []
    for i in range (0, num_of_days):
        li.append(end_date - timedelta(days=num_of_days-i-1))
    return li
def gen_today_date():
    return datetime.now().date()

def offset_date(date, days):
    return date + timedelta(days=days)

def gen_date_pair_by_days(last_n_days):
    return gen_date_pair(gen_today_date(), last_n_days)
def gen_date_pair_by_end_days(end_date, last_n_days):
    return gen_date_pair(end_date, last_n_days)