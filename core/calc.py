from common.utils import *
from core.load_data_from_akshare import *
from datetime import timedelta

def calc_single_fund_gain(data, buy_fee_rate, start_date, end_date, log=False):
    date_start_condition = data["净值日期"]>=start_date
    date_end_condition = data["净值日期"]<=end_date
    data = data[date_start_condition & date_end_condition].sort_values(by='净值日期', ascending=True)
    if (log):
        print("---数据---")
        print(data)
        print("--------")
    array = np.array(data["单位净值"])
    if (len(array)==0):
        return 0, 0, 0, 0, 0
    if (log):
        print("---净值---")
        print(array)
        print("--------")
    total_cost = 1000 * array.shape[0]
    amount_array = np.round(1000*(1-buy_fee_rate)/array, 2)

    total_price = np.sum(amount_array) * array[-1]
    total_gain = total_price - total_cost
    total_gain_rate = total_gain / total_cost

    #算下每个交易日的收益率
    gain_rate_per_day = total_gain_rate / array.shape[0]
    #预估全年交易日的收益率
    estimate_gain_rate_year = 251 * gain_rate_per_day
    return total_cost, total_gain, total_gain_rate, gain_rate_per_day, estimate_gain_rate_year

def calc_single_fund_gain_with_trend(data, buy_fee_rate, start_date, end_date, log=False):
    date_start_condition = data["净值日期"]>=start_date
    date_end_condition = data["净值日期"]<=end_date
    data = data[date_start_condition & date_end_condition].sort_values(by='净值日期', ascending=True)
    if (log):
        print("---数据---")
        print(data)
        print("--------")
    price_array = np.array(data["单位净值"])
    if (len(price_array)==0):
        return 0, 0, 0, 0, 0
    if (log):
        print("---净值---")
        print(price_array)
        print("--------")
    total_cost = 1000 * price_array.shape[0]
    amount_array = np.round(1000*(1-buy_fee_rate)/price_array, 2)

    total_price = np.sum(amount_array) * price_array[-1]
    total_gain = total_price - total_cost
    total_gain_rate = total_gain / total_cost

    #份数累加
    cum_amount_array = np.cumsum(amount_array)
    #当前持有价值
    cum_price_array = cum_amount_array * price_array
    #当前持有成本
    cum_cost_array = np.cumsum(np.full(price_array.shape[0], 1000))
    #日收益
    cum_gain_array = cum_price_array - cum_cost_array

    #算下每个交易日的收益率
    gain_rate_per_day = total_gain_rate / price_array.shape[0]
    #预估全年交易日的收益率
    estimate_gain_rate_year = 251 * gain_rate_per_day
    return total_cost, total_gain, total_gain_rate, gain_rate_per_day, estimate_gain_rate_year, cum_gain_array


# 计算指定基金定投收益（带缓存） 核心方法！！！
@lru_cache(maxsize=100000)
def calc_open_fund_gain(fund_code, start_date, end_date):
    data = load_open_fund_data(fund_code)
    buy_fee_rate = load_open_fund_buy_fee_rate(fund_code)
    return calc_single_fund_gain(data, buy_fee_rate, start_date, end_date)

# 计算指定基金定投收益（无缓存） 核心方法！！！
def calc_open_fund_gain_debug(fund_code, start_date, end_date, log=False):
    data = load_open_fund_data(fund_code)
    buy_fee_rate = load_open_fund_buy_fee_rate(fund_code)
    return calc_single_fund_gain(data, buy_fee_rate, start_date, end_date, log)

# 计算指定基金定投收益 带每日趋势（无缓存） 核心方法！！！
def calc_open_fund_gain_with_trend_debug(fund_code, start_date, end_date, log=False):
    data = load_open_fund_data(fund_code)
    buy_fee_rate = load_open_fund_buy_fee_rate(fund_code)
    return calc_single_fund_gain_with_trend(data, buy_fee_rate, start_date, end_date, log)


# 计算指定基金定投收益（无缓存） 核心方法！！！
def calc_open_fund_list_gain_debug(best_fund_code_list, end_date, log=False):
    total_cost = 0
    total_gain = 0
    start_date = end_date - timedelta(days=len(best_fund_code_list)-1)
    day_gain_map = {}
    fund_buy_date_map = {}
    pre_fund_code = best_fund_code_list[0]
    pre_start_date = start_date
    for i in range(1, len(best_fund_code_list)):
        fund_code = best_fund_code_list[i]
        if (pre_fund_code != fund_code):
            if (fund_buy_date_map.get(pre_fund_code) == None):
                fund_buy_date_map[pre_fund_code] = []
            pre_end_date = offset_date(start_date, i-1)
            fund_buy_date_map[pre_fund_code].append((pre_start_date, pre_end_date))
            pre_start_date = offset_date(start_date, i)
        pre_fund_code = fund_code
    if (fund_buy_date_map.get(pre_fund_code) == None):
        fund_buy_date_map[pre_fund_code] = []
    fund_buy_date_map[pre_fund_code].append((pre_start_date, end_date))
    if(log):
        print(fund_buy_date_map)

    for fund_code in fund_buy_date_map:
        buy_date_pair = fund_buy_date_map[fund_code]
        data = load_open_fund_data(fund_code)
        buy_fee_rate = load_open_fund_buy_fee_rate(fund_code)
        for (buy_start_date, buy_end_date) in buy_date_pair:
            single_cost, single_gain, _, _, _ = calc_single_fund_gain(data, buy_fee_rate, buy_start_date, buy_end_date, log)
            total_cost += single_cost
            total_gain += single_gain
    total_gain_rate = total_gain / total_cost
    return total_cost, total_gain, total_gain_rate
# 方法变动后重置缓存
# calc_open_fund_gain.cache_clear()