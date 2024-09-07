
import pandas as pd

from common import *
from constants import *

import akshare as ak

# 获取指定基金购买费率
def __ak_load_open_fund_buy_fee_rate(fund_code):
    all_funds = ak_load_open_funds_base_info()
    rate_str = all_funds[all_funds['基金代码']==fund_code]["手续费"].values[0]
    return float(rate_str.replace('%', '')) / 100.0

def __ak_load_all_open_funds_can_buy_code():
    all_funds = ak_load_open_funds_base_info()
    condition1 = all_funds['申购状态']!='暂停申购'
    condition2 = all_funds['申购状态']!='封闭期'
    return all_funds[condition1 & condition2]['基金代码'].values

def __disk_load_df_data(relative_data_path, file_name):
    # 获取数据存放位置
    absolute_data_path = os.path.abspath(relative_data_path)
    # 构建完整的 CSV 文件路径
    csv_file_path = os.path.join(absolute_data_path, file_name)
    # print("load file path:", csv_file_path)

    # 检查文件是否存在
    if not os.path.exists(csv_file_path):
        # print(f"The file {csv_file_path} does not exist!!")
        return None  # 或者抛出异常
    else:
        try:
            df_data_load = pd.read_csv(csv_file_path, encoding='utf-8-sig')  # 假设使用 utf-8-sig 编码
            return df_data_load
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")
            return None  # 或者重新抛出异常

def load_all_open_funds_base_info():
    return __disk_load_df_data(OPEN_FUNDS_BASE_DATA_PATH, ALL_OPEN_FUND_BASIC_FILE_NAME)

def load_all_open_funds_code():
    code_li = load_all_open_funds_base_info()['基金代码'].values
    return [f'{num:06}' for num in code_li]

def load_by_open_funds_code(fund_code_str):
    file_name = build_fund_code_file_name(fund_code_str)
    return __disk_load_df_data(OPEN_FUNDS_HISTORY_DATA_PATH, file_name)

def ak_load_by_open_funds_code(fund_code_str):
    return ak.fund_open_fund_info_em(symbol=fund_code_str, indicator="单位净值走势")

def ak_load_open_funds_base_info():
    return ak.fund_open_fund_daily_em()

if __name__ == '__main__':
    load_all_open_funds_code()