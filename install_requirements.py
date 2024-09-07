import subprocess
import os
from pathlib import Path

# 使用原始字符串来定义路径
requirements_path = 'requirements.txt'
command = [
    'pip', 'install', '-r', requirements_path,
    '-i', 'https://mirrors.aliyun.com/pypi/simple/'
]

if __name__ == '__main__':

    # 打印当前工作目录
    current_directory = os.getcwd()
    print("当前工作目录是:", current_directory)

    # 检查 requirements.txt 文件是否存在
    if not os.path.exists(requirements_path):
        print(f"文件不存在: {requirements_path}")
    else:
        requirements_path = Path('requirements.txt')
        # 读取文件内容
        content = requirements_path.read_text()
        # 打印文件内容
        print(content)

        # 启动子进程
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # 实时读取输出
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())

        # 等待进程结束
        process.wait()

        # 检查进程退出代码
        if process.returncode == 0:
            print("依赖安装成功")
        else:
            print("依赖安装失败")