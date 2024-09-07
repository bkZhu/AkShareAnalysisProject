# 结果展示方法
from common.utils import *


def show_result_list(fund_gain_list):
    print("todo")
def show_result(fund_gain):
    total_cost, total_gain, total_gain_rate, gain_rate_per_day, estimate_gain_rate_year = fund_gain
    res_str = f'总成本: {total_cost}，总盈利: {round(total_gain)}，总收益率: {to_percent_str(total_gain_rate)}，每日收益率: {to_percent_str(gain_rate_per_day)}，预计年化收益率: {to_percent_str(estimate_gain_rate_year)}'
    print(res_str)
    return res_str