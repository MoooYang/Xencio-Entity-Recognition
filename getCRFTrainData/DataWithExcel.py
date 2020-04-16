from base.DataBase import DataBase

import numpy as np
import pandas as pd
import xlrd
import xlsxwriter

import time
import datetime




class DataWithExcel_read(DataBase):
    
    def __init__(self, folder_name_read):

        DataBase.__init__(self, folder_name_work = folder_name_read)
        self.file_path_read = ""


    # 从excel中获取原始数据
    # 原始数据需要存放在项目文件夹中
    # 可以带index列和变量名行，如果有index列要求是第一列，变量名行要求是第一行
    # 返回值是二维的
    # with_title标识excel中是否有title，with_index同理
    def get_data(self, filename_read, return_type = "df", with_title = True, with_index = False):

        if with_title == True:  # 设定数据开始起点

            if with_index == True:

                data_start = (1, 1)

            else:

                data_start = (1, 0)

        else:

            if with_index == True:

                data_start = (0, 1)

            else:

                data_start = (0, 0)

        self.file_path_read = self.folder_path_work + "\\" + filename_read  # 获取原始数据文件的绝对路径

        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(now_time + "  开始读取数据：%s" %(filename_read))
        self.workbook_read = xlrd.open_workbook(self.file_path_read)
        self.worksheet_read = self.workbook_read.sheets()[0]
        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(now_time + "  数据读取完毕\n")

        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(now_time + "  开始转换数据格式")

        if with_title == True:  # 需要读取标题行

            if with_index == True:  # 需要读取index列

                column_title_list = self.worksheet_read.row_values(rowx = 0, start_colx = 1)  # 获取df每列的变量名称
                index_list = self.worksheet_read.col_values(colx = 0, start_rowx = 1)  # 获取df每行的index

            else:

                column_title_list = self.worksheet_read.row_values(rowx = 0, start_colx = 0)  

            data_nrows = self.worksheet_read.nrows - 1  # 数据行数

        else:

            if with_index == True:

                index_list = self.worksheet_read.col_values(colx = 0, start_rowx = 0)  

            data_nrows = self.worksheet_read.nrows  # 数据行数

        data_list = [[] for i in range(data_nrows)]  # 用于存储数据的二维list

        for row_index in range(data_nrows):  # 读取数据并放入data_array

            data_row_list_temp = self.worksheet_read.row_values(rowx = row_index + data_start[0], start_colx = data_start[1])  # 读取一行的数据
            
            for col_index in range(len(data_row_list_temp)):

                data_list[row_index].append(data_row_list_temp[col_index])  

        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(now_time + "  数据格式转换完毕\n")

        if return_type == "df":

            if with_title == True:

                if with_index == True:

                    data_df = pd.DataFrame(data_list, index = index_list, columns = column_title_list)

                else:

                    data_df = pd.DataFrame(data_list, columns = column_title_list)

            else:

                if with_index == True:

                    data_df = pd.DataFrame(data_list, index = index_list)

                else:

                    data_df = pd.DataFrame(data_list)

            return data_df

        elif return_type == "list":

            return data_list

        else:

            data_array = np.array(data_list)

            return data_array




class DataWithExcel_write(DataBase):

    def __init__(self, folder_name_write):

        DataBase.__init__(self, folder_name_work = folder_name_write)
        self.file_path_write = ""


    # 把数据矩阵写入row, col为起点的excel表格中
    # data_list必须是一个二维嵌套list
    def matrix_to_excel(self, data_list, worksheet, row, col):

        for i in range(len(data_list)):

            worksheet.write_row(row + i, col, data_list[i])


    # 把一个df写入excel
    # filename记得加文件后缀
    # todo: 写入任意位置
    def df_to_excel(self, data_df, filename_write):

        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(now_time + "  开始写入数据")

        self.file_path_write = self.folder_path_work + "\\" + filename_write
        workbook_write = xlsxwriter.Workbook(self.file_path_write)
        worksheet = workbook_write.add_worksheet("处理结果")

        title_list = [list(data_df.columns)]
        data_list = np.array(data_df).tolist()

        self.matrix_to_excel(data_list = title_list, worksheet = worksheet, row = 0, col = 0)  # 把标题写入excel
        self.matrix_to_excel(data_list = data_list, worksheet = worksheet, row = 1, col = 0)  # 把数据写入excel

        workbook_write.close()

        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(now_time + "  数据写入完毕\n")


    # 把一个df_list写入excel的不同worksheet
    # filename记得加文件后缀
    def df_list_to_excel(self, data_df_list, sheetname_list, filename_write):

        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(now_time + "  开始写入数据\n")

        self.file_path_write = self.folder_path_work + "\\" + filename_write
        workbook_write = xlsxwriter.Workbook(self.file_path_write)
        count = 0

        for sheetname in sheetname_list:

            now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(now_time + "  开始写入表：%s" %(sheetname))

            worksheet = workbook_write.add_worksheet(sheetname)

            title_list = [list(data_df_list[count].columns)]
            data_list = np.array(data_df_list[count]).tolist()

            self.matrix_to_excel(data_list = title_list, worksheet = worksheet, row = 0, col = 0)  # 把标题写入excel
            self.matrix_to_excel(data_list = data_list, worksheet = worksheet, row = 1, col = 0)  # 把数据写入excel

            count += 1

            now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(now_time + "  写入完毕\n")

        workbook_write.close()

        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(now_time + "  数据写入完毕\n")
