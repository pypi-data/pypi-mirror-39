"""
管理日志记录工具；
"""
import time
import os


# 日志管理者；
class LogHandler(object):

    def __init__(self,
                 date_format="%Y-%m-%d--%H:%M:%S",
                 log_dir="logs",
                 print_symbol=True):
        self.date_format = date_format
        self.log_dir = log_dir
        self.print_symbol = print_symbol

        # 创建文件夹；
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

    # 定位目标日志文件，如果不存在则创建该文件；
    def locate_log(self):
        date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        return os.path.join(self.log_dir, date)

    # 写日志;
    def __write_log(self, write_type, *args):
        log_str = ' '.join(args)
        write_log = time.strftime(self.date_format, time.localtime(time.time())) + "---" + write_type.ljust(7, '-') \
                    + "--" + log_str + '\n'

        if self.print_symbol:
            print(write_log[:-1])

        with open(self.locate_log(), 'a') as writer:
            writer.write(write_log)

    # 写debug级别日志；
    def debug(self, *args):
        self.__write_log("DEBUG", *args)

    # 写info级别日志；
    def info(self, *args):
        self.__write_log("INFO", *args)

    # 写warning级别日志；
    def warning(self, *args):
        self.__write_log("WARNING", *args)

    # 写error级别日志；
    def error(self, *args):
        self.__write_log("ERROR", *args)

    def __show_log(self, show_type, day):
        file_path = os.path.join(self.log_dir, day)

        # 查找该控制器下字符串中级别信息所在的索引,用于查找字符串；
        # +3是因为日志在时间信息后有3个'-'符号；
        index = len(time.strftime(self.date_format, time.localtime(time.time()))) + 3

        with open(file_path, 'r') as reader:
            info_list = reader.readlines()
            info_list = [info for info in info_list if info[index:].startswith(show_type)]
            print(''.join(info_list))

    # 显示某日所有的debug级别的日志信息；
    def show_debug(self, day=time.strftime('%Y-%m-%d', time.localtime(time.time()))):
        self.__show_log("DEBUG", day)

    # 显示某日所有的info级别的日志信息；
    def show_info(self, day=time.strftime('%Y-%m-%d', time.localtime(time.time()))):
        self.__show_log("INFO", day)

    # 显示某日所有的warning级别的日志信息；
    def show_warning(self, day=time.strftime('%Y-%m-%d', time.localtime(time.time()))):
        self.__show_log("WARNING", day)

    # 显示某日所有的error级别的日志信息；
    def show_error(self, day=time.strftime('%Y-%m-%d', time.localtime(time.time()))):
        self.__show_log("ERROR", day)

    def __str__(self):
        return self.date_format

