import os

def update_init(file_path):
    # 获取当前目录下的所有 .py 文件（不包括 __init__.py）
    modules = [f for f in os.listdir(file_path) if f.endswith('.py') and f != '__init__.py']
    # 创建或更新 __init__.py 文件
    with open(os.path.join(file_path, '__init__.py'), 'w') as f:
        for module in modules:
            f.write(f'from .{module[:-3]} import *\n')
        print(f"Updated __init__.py in {file_path}")

if __name__ == '__main__':
    # 用法示例
    # 假设你的包路径是 'my_package'
    update_init('common')
    update_init('core')