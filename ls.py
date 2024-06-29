import os
import time
import argparse
from rich import print


def get_file_info(file_path, show_modified, show_viewed):
    """获取文件信息，减少系统调用次数"""
    stat_result = os.stat(file_path)
    file_size = stat_result.st_size
    ext = os.path.splitext(file_path)[1]

    # 只有当需要时才计算时间戳
    last_modified_time = time.strftime(
        "%Y-%m-%d %H:%M", time.localtime(stat_result.st_mtime)) if show_modified else ""
    last_view_time = time.strftime(
        "%Y-%m-%d %H:%M:%S", time.localtime(stat_result.st_atime)) if show_viewed else ""

    return file_size, last_modified_time, last_view_time, ext


# 添加命令行参数支持，可以指定目录，默认为当前目录
parser = argparse.ArgumentParser(description="列出指定目录下的所有文件和文件夹")
parser.add_argument("directory", nargs='?', default='.', help="要列出的目录")
parser.add_argument("-m", "--modified", action="store_true", help="显示最后修改时间")
parser.add_argument("-v", "--viewed", action="store_true", help="显示最后访问时间")
parser.add_argument("--version", action="version", version='%(prog)s 3.0.1')

args = parser.parse_args()

# 直接使用给定的目录，避免不必要的chdir调用
directory = args.directory

# 使用os.scandir()代替os.listdir()和os.stat()，它更高效
with os.scandir(directory) as it:
    for entry in it:
        if entry.is_dir():
            print(f"[cyan]{entry.name}[/cyan][green](目录)[/green]")
        else:
            file_size, last_modified_time, last_view_time, ext = get_file_info(
                entry.path, args.modified, args.viewed)
            print(f"""[magenta]{entry.name}[/magenta] [yellow]({file_size}字节)[/yellow] [green](文件)[/green] [black]({last_modified_time}{'最后修改时间:' if last_modified_time else ''}{'最后查看时间'+last_view_time+' ' if last_view_time else ''}{ext if ext else "无后缀"})[/black]""")
