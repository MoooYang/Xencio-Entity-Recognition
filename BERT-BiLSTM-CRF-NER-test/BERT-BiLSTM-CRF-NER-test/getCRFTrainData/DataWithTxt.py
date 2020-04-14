from base.DataBase import DataBase

import numpy as np

import time
import datetime




class DataWithTxt_read(DataBase):

    # folder_name_read: 文件夹的名字，需要放在和Run同级目录下
    def __init__(self, folder_name_read):

        DataBase.__init__(self, folder_name_work = folder_name_read)
        self.file_path_read = ""


    # 读取一行一项的标准txt文件，输出list
    def get_data(self, filename_read, return_type = "list"):

        self.file_path_read = self.folder_path_work + "\\" + filename_read  # 获取原始数据文件的绝对路径

        with open(self.file_path_read, 'r', encoding = "utf-8") as file_to_read:

            data_temp_list = file_to_read.read().rstrip().split("\n")  # 去除所有右侧的空白字符，然后根据回车划分

        if return_type == "list":

            return data_temp_list

        elif return_type == "array":

            return np.array(data_temp_list)




class DataWithTxt_write(DataBase):

    def __init__(self, folder_name_write):

        DataBase.__init__(self, folder_name_work = folder_name_write)
        self.file_path_write = ""


    # 一个字符串写入一行
    def str_to_txt(self, data_str, filename_write):

        self.file_path_write = self.folder_path_work + "\\" + filename_write

        with open(self.file_path_write, 'w') as file_to_write:

            file_to_write.write(data_str)


    # 一个列表写入txt，写入后追加一个规定的分隔符，默认为回车
    def list_to_txt(self, data_list, filename_write, separator = "\n"):

        self.file_path_write = self.folder_path_work + "\\" + filename_write

        with open(self.file_path_write, 'w', encoding = "utf-8") as file_to_write:

            file_to_write.write(separator.join(data_list))
