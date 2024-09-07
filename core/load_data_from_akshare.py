from functools import lru_cache
import akshare as ak

# 获取指定基金数据
@lru_cache(maxsize=100000)
def load_open_fund_data(fund_code):
    return ak.fund_open_fund_info_em(symbol=fund_code, indicator="单位净值走势")

# 获取指定基金购买费率
@lru_cache(maxsize=100000)
def load_open_fund_buy_fee_rate(fund_code):
    all_funds = load_all_open_fund_basic_info()
    rate_str = all_funds[all_funds['基金代码']==fund_code]["手续费"].values[0]
    return float(rate_str.replace('%', '')) / 100.0

@lru_cache(maxsize=128)
def load_all_open_fund_basic_info():
    return ak.fund_open_fund_daily_em()

@lru_cache(maxsize=128)
def load_all_open_funds_can_buy_code():
    all_funds = load_all_open_fund_basic_info()
    condition1 = all_funds['申购状态']!='暂停申购'
    condition2 = all_funds['申购状态']!='封闭期'
    return all_funds[condition1 & condition2]['基金代码'].values