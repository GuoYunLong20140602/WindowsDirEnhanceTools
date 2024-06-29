import sys
import os
import time
from rich import print
if len(sys.argv) == 1:
    # 获取当前目录下的文件名和信息
    files = os.listdir(os.getcwd())
else:
    # 获取指定目录下的文件名和信息（如果存在）
    files = os.listdir(sys.argv[1])

a = []
b = []
for file in files:
    if os.path.isdir(file):
        a.append(file)
    elif os.path.isfile(file):  # 如果是文件，则打印文件名,大小信息,最后修改时间,后缀名信息
        # 打印文件名和大小信息（可选）
        b.append(file)
files = sorted(a) + sorted(b)
for file in files:
    if os.path.isdir(file):
        print(f"[cyan]{file}[/cyan][green](目录)[/green]")
    elif os.path.isfile(file):
        last_modified_time = time.strftime("%Y-%m-%d %H:%M",
                                           time.localtime(os.path.getmtime(file)))
        last_view_time = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(os.path.getatime(file)))
        print(
            f"[magenta]{file}[/magenta] [yellow]({os.path.getsize(file)}字节)[/yellow] [green](文件)[/green] [black](修改时间:{last_modified_time})({os.path.splitext(file)[1]})[/black]")  # 打印文件名,大小信息,最后修改时间,后缀名信息
