from core import *

def save_df_to_csv(df_data, relative_data_path, file_name):
    # 获取数据存放位置
    absolute_data_path = os.path.abspath(relative_data_path)
    # 构建完整的 CSV 文件路径
    csv_file_path = os.path.join(absolute_data_path, file_name)
    # print("save file path:", csv_file_path)

    # 检查路径是否存在，如果不存在则创建
    if not os.path.exists(absolute_data_path):
        print(f"The path {absolute_data_path} does not exist. Creating it...")
        os.makedirs(absolute_data_path)

    # 检查路径是否确实是一个目录
    if os.path.isdir(absolute_data_path):
        # 保存 DataFrame 到 CSV
        df_data.to_csv(csv_file_path, index=False, encoding='utf-8-sig')
        # print(f"Data saved to {csv_file_path}")
    else:
        print(f"The path {absolute_data_path} is not a directory.")


## save all open funds data to disk
def save_latest_open_fund_base_data():
    df_data = load_all_open_funds_base_info()
    save_df_to_csv(df_data, OPEN_FUNDS_BASE_DATA_PATH, ALL_OPEN_FUND_BASIC_FILE_NAME)

def save_latest_open_fund_all_history_data(fund_code_str, backfill):
    #避免重复save
    if backfill:
        df_data = load_by_open_funds_code(fund_code_str)
        if df_data is None or len(df_data) == 0:
            df_data = ak_load_by_open_funds_code(fund_code_str)
    else:
        df_data = ak_load_by_open_funds_code(fund_code_str)
    if df_data is None or len(df_data) == 0:
        print(f"fund_code:{fund_code_str} NO DATA skip")
        return
    file_name = build_fund_code_file_name(fund_code_str)
    save_df_to_csv(df_data, OPEN_FUNDS_HISTORY_DATA_PATH, file_name)


def worker(code, finish_li, total, start_time, progress_lock):
    import time
    save_latest_open_fund_all_history_data(code, True)
    # 使用锁来安全地更新进度
    with progress_lock:
        finish_li.append(code)
        #进度
        current_progress = len(finish_li) / total * 100
        # 计算平均加载时间
        sum_cost_time = time.time() - start_time
        average_time = sum_cost_time / len(finish_li)
        # 计算预期剩余时间
        remaining_time = (total - len(finish_li)) * average_time
        if len(finish_li) % 10 == 0:
            print(f"Progress: {len(finish_li)}/{total} - Code: {code} - {current_progress:.2f}%")
            print(f"cost time: {sum_cost_time:.2f} sec")
            print(f"Estimated remaining time: {remaining_time/60:.2f} min")

def save_all():
    import threading
    import time
    from concurrent.futures import ThreadPoolExecutor

    all_code = load_all_open_funds_code()
    start_time = time.time()
    total = len(all_code)
    finish_li = []
    progress_lock = threading.Lock()

    # 创建一个线程池，2个线程大约要拉2小时
    with ThreadPoolExecutor(max_workers=2) as executor:
        # 提交所有任务到线程池
        futures = [executor.submit(worker, code, finish_li, total, start_time, progress_lock) for code in all_code]

    # 等待所有线程完成
    for future in futures:
        future.result()

    # 打印最终的进度
    print(f"All tasks completed.")

if __name__ == '__main__':
    print("test")
    # save_latest_open_fund_base_data()
    # save_all()