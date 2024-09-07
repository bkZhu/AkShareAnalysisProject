from core import *
import os
import pandas as pd
from constants import *


def save_df_to_csv(df_data, relative_data_path, file_name):
    # 获取数据存放位置
    absolute_data_path = os.path.abspath(relative_data_path)
    # 构建完整的 CSV 文件路径
    csv_file_path = os.path.join(absolute_data_path, file_name)
    print("save file path:", csv_file_path)

    # 检查路径是否存在，如果不存在则创建
    if not os.path.exists(absolute_data_path):
        print(f"The path {absolute_data_path} does not exist. Creating it...")
        os.makedirs(absolute_data_path)

    # 检查路径是否确实是一个目录
    if os.path.isdir(absolute_data_path):
        # 保存 DataFrame 到 CSV
        df_data.to_csv(csv_file_path, index=False, encoding='utf-8-sig')
        print(f"Data saved to {csv_file_path}")
    else:
        print(f"The path {absolute_data_path} is not a directory.")


## save all open funds data to disk
def save_latest_open_fund_base_data():
    df_data = load_all_open_fund_basic_info()
    save_df_to_csv(df_data, OPEN_FUNDS_BASE_DATA_PATH, ALL_OPEN_FUND_BASIC_FILE_NAME)

def build_fund_code_file_name(fund_code_str):
    return fund_code_str + ".csv"

def save_latest_open_fund_all_history_data(fund_code_str):
    df_data = load_open_fund_data(fund_code_str)
    file_name = build_fund_code_file_name(fund_code_str)
    save_df_to_csv(df_data, OPEN_FUNDS_HISTORY_DATA_PATH, file_name)


if __name__ == '__main__':
    save_latest_open_fund_base_data()
    # save_latest_open_fund_all_history_data("270042")
