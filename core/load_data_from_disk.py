import os
import pandas as pd

from constants import *


def load_df_data_from_disk(relative_data_path, file_name):
    # 获取数据存放位置
    absolute_data_path = os.path.abspath(relative_data_path)
    # 构建完整的 CSV 文件路径
    csv_file_path = os.path.join(absolute_data_path, file_name)
    print("load file path:", csv_file_path)

    # 检查文件是否存在
    if not os.path.exists(csv_file_path):
        print(f"The file {csv_file_path} does not exist!!")
        return None  # 或者抛出异常
    else:
        try:
            # 尝试读取 CSV 文件
            df_data_load = pd.read_csv(csv_file_path, encoding='utf-8-sig')  # 假设使用 utf-8-sig 编码
            return df_data_load
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")
            return None  # 或者重新抛出异常

if __name__ == '__main__':
    df = load_df_data_from_disk(OPEN_FUNDS_BASE_DATA_PATH, ALL_OPEN_FUND_BASIC_FILE_NAME)
    if df is not None:
        print(df)