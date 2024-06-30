import os
import datetime
import argparse
from rich import print


def ls():
    def get_file_info(file_path, show_modified, show_viewed, show_ext):
        """获取文件信息，减少系统调用次数"""
        stat_result = os.stat(file_path)
        file_size = format_size(stat_result.st_size)
        ext = os.path.splitext(file_path)[1] if show_ext else ""

        # 只有当需要时才计算时间戳
        last_modified_time = "" if not show_modified else datetime.datetime.fromtimestamp(
            stat_result.st_mtime).strftime("%Y-%m-%d %H:%M") + " "
        last_view_time = "" if not show_viewed else datetime.datetime.fromtimestamp(
            stat_result.st_atime).strftime("%Y-%m-%d %H:%M") + " "
        return file_size, last_modified_time, last_view_time, ext

    def format_size(size):
        """格式化文件大小，转换为更友好的单位"""
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        unit_index = 0
        while size >= 1024 and unit_index < len(units)-1:
            size /= 1024
            unit_index += 1
        return f"{round(size, 2)} {units[unit_index]}"

    # 添加命令行参数支持，可以指定目录，默认为当前目录
    parser = argparse.ArgumentParser(description="列出指定目录下的所有文件和文件夹")
    parser.add_argument("directory", nargs='?', default='.', help="要列出的目录")
    parser.add_argument("-m", "--modified",
                        action="store_true", help="显示最后修改时间")
    parser.add_argument(
        "-v", "--viewed", action="store_true", help="显示最后访问时间")
    parser.add_argument("--version", action="version",
                        version='%(prog)s 3.2.1', help="显示版本信息")  # 添加版本信息支持
    parser.add_argument("-e", "--ext", action="store_false", help="显示文件类型")
    parser.add_argument("-t", "--type", action="store_true",
                        help="显示是文件还是目录")  # 添加文件类型选项
    args = parser.parse_args()

    # 直接使用给定的目录，避免不必要的chdir调用
    directory = args.directory

    files = []

    # 使用os.scandir()代替os.listdir()和os.stat()，它更高效
    with os.scandir(directory) as it:
        for entry in it:
            if entry.is_dir():
                print(
                    f"[cyan]{entry.name}[/cyan][green]{'(目录)' if args.type else ''}[/green]")
            else:
                files.append(entry)

    # 输出文件
    for file_entry in files:
        file_size, last_modified_time, last_view_time, ext = get_file_info(
            file_entry.path, args.modified, args.viewed, args.ext)
        extra_info = (
            f"({'' if not last_modified_time else '修改时间: ' + last_modified_time}"
            f"{'' if not last_view_time else '查看时间: ' + last_view_time}"
            f"{ext})"
        ) if last_modified_time or last_view_time or ext else ""
        print(
            f"""[magenta]{file_entry.name}[/magenta] [yellow]({file_size})[/yellow] [green]{'(文件)' if args.type else ''}[/green] [black]{extra_info}[/black]""")


if __name__ == "__main__":
    s1 = datetime.datetime.now()
    ls()
    print(datetime.datetime.now() - s1)
