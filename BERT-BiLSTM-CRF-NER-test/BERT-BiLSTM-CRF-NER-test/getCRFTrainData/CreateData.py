from base.Keyword import KeywordManager
from getCRFTrainData.DataWithExcel import DataWithExcel_read, DataWithExcel_write
from getCRFTrainData.DataWithTxt import DataWithTxt_read, DataWithTxt_write
from tools.CommonTools import timer
from tools.CommonTools import clean_the_same
from tools.CommonTools import sub_str_list_with_regexp, keyword_matrix_in_word, string_cut_off_from_key
from tools.CommonTools import tuple_list_find_key_index, merge_tuple_list
from tools.CommonTools import sample_from_list

from sklearn.model_selection import train_test_split
from tqdm import tqdm
import fool
import pandas as pd
import numpy as np

import datetime
import time
import copy




class CreateCorpName():

    def __init__(self, folder_name_read, folder_name_write, folder_name_param):

        self.keyword_read_obj = KeywordManager(folder_name_read = folder_name_param)
        self.excel_read_obj = DataWithExcel_read(folder_name_read = folder_name_read)
        self.excel_write_obj = DataWithExcel_write(folder_name_write = folder_name_write)
        self.txt_read_obj = DataWithTxt_read(folder_name_read = folder_name_read)
        self.txt_write_obj = DataWithTxt_write(folder_name_write = folder_name_write)

        self.keyword_read_obj.get_keyword_lawtype(filename_read = "lawtype_keyword.xlsx")


    # 读取一个txt文件，然后去重输出为标准格式的txt
    def remove_duplicate(self, filename_read_txt, filename_write_txt):

        data_list = self.txt_read_obj.get_data(filename_read = filename_read_txt, return_type = "list")
        data_list_unique, _ = clean_the_same(data_list, orig_sort = True)
        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(now_time + "  删除重复项数量：%d" %(len(data_list) - len(data_list_unique)))

        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(now_time + "开始写入txt")

        self.txt_write_obj.list_to_txt(data_list = data_list_unique, filename_write = filename_write_txt, separator = "\n")

        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(now_time + "写入完毕\n")


    # 读取一个excel文件指定列，然后输出为标准格式的txt
    # 下标从0开始
    def excel_col_to_txt(self, filename_read_excel, filename_write_txt, with_title = True, with_index = False, col_num = 0):

        data_array_all = self.excel_read_obj.get_data(filename_read = filename_read_excel, \
            return_type = "array", with_title = with_title, with_index = with_index)
        data_list = data_array_all[:, col_num].tolist()
        self.txt_write_obj.list_to_txt(data_list = data_list, filename_write = filename_write_txt, separator = "\n")


    # 输入一个企业名list，先去除所有空白字符，再提取带有明显企业关键字的那些，然后获取标准企业名list
    @timer
    def get_standard_corp_name(self, corp_name_list):

        corp_name_list = sub_str_list_with_regexp(str_list = corp_name_list, regexp = "\s", target = "")  # 先去垃圾字符
        corp_name_list = sub_str_list_with_regexp(str_list = corp_name_list, regexp = "\(", target = "（")  # 括号标准化
        corp_name_list = sub_str_list_with_regexp(str_list = corp_name_list, regexp = "\)", target = "）")  
        corp_name_list = sub_str_list_with_regexp(str_list = corp_name_list, regexp = "（.*?）", target = "")  # 括号里的不要了
        corp_name_list = sub_str_list_with_regexp(str_list = corp_name_list, regexp = "（", target = "")  # 去除单边括号
        corp_name_list = sub_str_list_with_regexp(str_list = corp_name_list, regexp = "）", target = "")  

        corp_name_list_standard = ["" for i in range(len(corp_name_list))]
        valid_count = 0

        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(now_time + "  开始提取标准公司名称：")

        for corpName in tqdm(corp_name_list, ncols = 75):

            result_temp = keyword_matrix_in_word(keyword_matrix = self.keyword_read_obj.lawtype_keyword_matrix, string = corpName)  # 矩阵关键字匹配

            if result_temp[0] == True:

                corp_name_list_standard[valid_count], _ = string_cut_off_from_key(string = corpName, key = result_temp[1], \
                    appear_type = "first", cut_type = "after", include = False)  # 第一次出现关键字后面的都不要了
                valid_count = valid_count + 1

        corp_name_list_standard = corp_name_list_standard[0 : valid_count]

        return corp_name_list_standard


    # 利用fool，对一个list的公司名称提取经营范围
    # 要求输入是标准企业，且无分支机构，无括号
    # 先做分词，提取最后一个nz之后的内容，然后经过一定的规则处理合并为一个字符串
    # 最后去除尾部的公司关键字
    @timer
    def get_businessScope_list_with_fool(self, corp_name_list):

        businessScope_list = ["" for i in range(len(corp_name_list))]
        count = 0

        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(now_time + "  开始提取经营范围：")

        for corpName_str in tqdm(corp_name_list, ncols = 75):

            data_tuple_list_single = fool.pos_cut(corpName_str)[0]
            last_nz_index_single = tuple_list_find_key_index(tuple_list = data_tuple_list_single, axis = 1, key = "nz", appear_type = "last")  # 最后一个nz标签位置

            if last_nz_index_single != -1 and last_nz_index_single + 1 < len(data_tuple_list_single) \
                and len(data_tuple_list_single[last_nz_index_single + 1][0]) > 1:  # 存在nz且最后一个nz后第一个分词字段不是单字，且nz不是最后一个

                tuple_list_withoutNZ = data_tuple_list_single[last_nz_index_single + 1 :]
                first_ns_index_single = tuple_list_find_key_index(tuple_list = tuple_list_withoutNZ, axis = 1, key = "ns", appear_type = "first")  # 去除nz后第一个ns标签位置

                if first_ns_index_single == 0:

                    tuple_list_withoutNZ = tuple_list_withoutNZ[1 :]

                elif first_ns_index_single != -1:

                    tuple_list_withoutNZ = tuple_list_withoutNZ[0: first_ns_index_single]

                businessScope_temp = merge_tuple_list(tuple_list = tuple_list_withoutNZ, axis = 0)
                lawtype_key_result_temp = keyword_matrix_in_word(keyword_matrix = self.keyword_read_obj.lawtype_keyword_matrix, \
                    string = businessScope_temp)  # 矩阵关键字匹配
                businessScope_temp, _ = string_cut_off_from_key(string = businessScope_temp, key = lawtype_key_result_temp[1], \
                    appear_type = "first", cut_type = "after", include = True)  # 剔除末尾的公司类型标识

                if businessScope_temp != "" and len(businessScope_temp) > 1:  # 经营范围只有一个字的也去掉

                    businessScope_list[count] = businessScope_temp
                    count += 1

        return businessScope_list[: count]


    # 从完整公司名称的数据源文件中提取经营范围，并保存
    # 原文件名为.txt或.xlsx结尾
    # excel文件要求把数据放在第一列，输入输出都带标题
    @timer
    def get_businessScope(self, filename_read, filename_write):

        filetype_read, _ = string_cut_off_from_key(string = filename_read, key = ".", appear_type = "last", cut_type = "before", include = True)
        filetype_write, filetype_write_key_index = string_cut_off_from_key(string = filename_write, key = ".", appear_type = "last", cut_type = "before", include = True)

        if filetype_read == "txt":

            data_list = self.txt_read_obj.get_data(filename_read = filename_read, return_type = "list")

        elif filetype_read == "xlsx":

            data_list = self.excel_read_obj.get_data(filename_read = filename_read, return_type = "array", with_title = True, with_index = False)[:, 0].tolist()

        data_list = self.get_standard_corp_name(corp_name_list = data_list)
        data_list = self.get_businessScope_list_with_fool(corp_name_list = data_list)
        data_list, different_data_num = clean_the_same(data_list = data_list, orig_sort = True)
        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(now_time + "  共提取不同经营范围数量：%d" %(different_data_num))

        if filetype_write == "txt":

            self.txt_write_obj.list_to_txt(data_list = data_list, filename_write = filename_write, separator = "\n")

        elif filetype_write == "xlsx":

            data_df = pd.DataFrame({"businessScope" : data_list})
            self.excel_write_obj.df_to_excel(data_df = data_df, filename_write = filename_write)

        elif filetype_write_key_index == -1:

            data_df = pd.DataFrame({"businessScope" : data_list})
            self.txt_write_obj.list_to_txt(data_list = data_list, filename_write = filename_write + ".txt", separator = "\n")
            self.excel_write_obj.df_to_excel(data_df = data_df, filename_write = filename_write + ".xlsx")


    # 用四个字符串列表生成raw训练集列表
    # 每个城市，随机选取uniqueName_list总长度的1/5取整，再随机选一个lawType，最后取经营范围列表总长度的1/uniqueName_list_each_city取整进行遍历组合
    # raw训练集合列表元素为字符串，每个字符串用“|”分割不同部分，可以为空
    # 每个元素为一个生成的公司
    def get_trainData_raw_list(self, place_str_list, uniqueName_str_list, businessScope_str_list, lawType_str_list):

        trainData_raw_list = []

        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(now_time + "  开始合成raw训练集：")

        for i in tqdm(range(len(place_str_list)), ncols = 75):

            uniqueName_list_each_city = sample_from_list(n = int(len(place_str_list) / 30) + 1, data_list = uniqueName_str_list, replace = False)  # 每个城市，随机选取place_str_list总长度的1/30向上取整
            lawType_each_city_list = [sample_from_list(n = 1, data_list = lawType_str_list, replace = False)[0] for i in range(len(uniqueName_list_each_city))]  # 随机选一个lawType

            for j in range(len(uniqueName_list_each_city)):

                businessScope_list_each_corp = sample_from_list(n = int(len(businessScope_str_list) / len(uniqueName_list_each_city)) + 1, data_list = businessScope_str_list, replace = False)  # 取经营范围列表总长度的1/uniqueName_list_each_city向上取整进行遍历组合

                for k in range(len(businessScope_list_each_corp)):

                    trainData_raw_list_single = [place_str_list[i], "GEO", uniqueName_list_each_city[j], "UNN", businessScope_list_each_corp[k], "BUS", lawType_each_city_list[j], "LAT"]
                    trainData_raw_list.append("|".join(trainData_raw_list_single))

        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(now_time + "  合成完毕\n")

        return trainData_raw_list


    # 用四个txt文件生成raw训练集并输出到txt
    def get_trainData_raw(self, place_filename_txt, uniqueName_filename_txt, businessScope_filename_txt, lawType_filename_txt, trainData_raw_filename_txt):

        place_str_list = self.txt_read_obj.get_data(filename_read = place_filename_txt, return_type = "list")
        uniqueName_str_list = self.txt_read_obj.get_data(filename_read = uniqueName_filename_txt, return_type = "list")
        businessScope_str_list = self.txt_read_obj.get_data(filename_read = businessScope_filename_txt, return_type = "list")
        lawType_str_list = self.txt_read_obj.get_data(filename_read = lawType_filename_txt, return_type = "list")

        trainData_raw_list = self.get_trainData_raw_list(place_str_list = place_str_list, uniqueName_str_list = uniqueName_str_list, \
            businessScope_str_list = businessScope_str_list, lawType_str_list = lawType_str_list)  # 获取raw训练集列表

        self.txt_write_obj.list_to_txt(data_list = trainData_raw_list, filename_write = trainData_raw_filename_txt, separator = "\n")


    # 给定一个字符串，按指定准则切割成列表，并在最后加上指定的标签
    @staticmethod
    def string_plus_sth_to_list(string, tag, separator_for_sth = " ", tag_mode = "BMEWO"):

        list_from_str = []

        if string == "":

            return list_from_str

        list_from_str.append(string[0] + separator_for_sth + "B-" + tag)
        string = string[1 :]

        if tag_mode == "BMEWO":

            if string == "":

                return list_from_str

            elif len(string) == 1:

                list_from_str.append(string[0] + separator_for_sth + "E-" + tag)

                return list_from_str

            else:

                for i in range(len(string) - 1):

                    list_from_str.append(string[i] + separator_for_sth + "M-" + tag)

                list_from_str.append(string[-1] + separator_for_sth + "E-" + tag)

                return list_from_str

        elif tag_mode == "BIO":

            for i in range(len(string)):

                list_from_str.append(string[i] + separator_for_sth + "I-" + tag)

            return list_from_str


    # 给定公司名称的字段，生成单个元素的训练集列表，每个元素就是类似"王 B-PER"这样的结构
    # 最后加上一个空字符
    # create_mode表示单个词的构成方式，可以改成任意形式，如["uniqueName", "place", "lawType"]
    # 对应的tag_list就是：["UNN", "GEO", "LAT"]
    # corpName_dict不需要有固定的形式
    def get_trainData_single(self, corpName_dict, create_mode = ["place", "uniqueName", "businessScope", "lawType"], tag_list = ["GEO", "UNN", "BUS", "LAT"], separator_for_tags = " ", tag_mode = "BIO"):

        nparts = len(create_mode)  # 一共需要几个字段 
        parts_list_to_use = []
        train_data_list_single = []
        
        for i in range(nparts):

            parts_list_to_use.append(corpName_dict[create_mode[i]])
            parts_list_train = self.string_plus_sth_to_list(string = corpName_dict[create_mode[i]], tag = tag_list[i], separator_for_sth = separator_for_tags, tag_mode = tag_mode)
            train_data_list_single.extend(copy.deepcopy(parts_list_train))

        train_data_list_single.extend([""])

        return train_data_list_single


    # raw数据集的list转换为CRF++数据集list
    # 返回也是list
    # create_mode_dict要求按你需要的顺序建立，如1, 2, 0, 3...
    def data_raw_to_CRF(self, data_raw_list, create_mode_dict = {0 : "place", 1 : "uniqueName", 2 : "businessScope", 3 : "lawType"}, separator_for_tags = " ", tag_mode = "BIO"):

        data_list = []
        create_mode = list(create_mode_dict.values())
        create_order = list(create_mode_dict.keys())
        tag_list_orig = [data_raw_list[0].split("|")[2 * i + 1] for i in range(int(len(create_mode_dict)))]
        tag_list = [tag_list_orig[create_order[i]] for i in range(len(tag_list_orig))]

        for data_raw_single in tqdm(data_raw_list, ncols = 75):

            data_raw_single_list = data_raw_single.split("|")  # 单个数据转为列表，列表格式为[place, "GEO", uniqueName, "UNN", businessScope, "BUS", lawType, "LAT"]这样的
            data_raw_single_dict = {}  

            for i in range(len(create_mode_dict)):  # 单个数据列表转为字典

                data_raw_single_dict[create_mode[i]] = data_raw_single_list[2 * create_order[i]]

            data_list_single = self.get_trainData_single(corpName_dict = data_raw_single_dict, create_mode = create_mode, tag_list = tag_list, \
                separator_for_tags = separator_for_tags, tag_mode = tag_mode)  # 打上标签
            data_list.extend(copy.deepcopy(data_list_single))  # 拼接成一个一维列表

        return data_list


    # 读取raw训练集的txt文件，按照给定的比例输出CRF++训练集、测试集为txt格式，以及对应训练集和测试集的raw数据，以便进一步划分验证集
    def get_train_test_Data(self, trainData_raw_filename_txt, create_mode_dict = {0 : "place", 1 : "uniqueName", 2 : "businessScope", 3 : "lawType"}, test_size = 0.2, separator_for_tags = " ", tag_mode_list = ["BIO", "BMEWO"]):

        data_raw_list = self.txt_read_obj.get_data(filename_read = trainData_raw_filename_txt, return_type = "list")

        if test_size != 0 and test_size != 1:

            now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(now_time + "  开始划分训练集：")
            trainData_raw_list, testData_raw_list = train_test_split(data_raw_list, test_size = test_size, random_state = int(time.time()), shuffle = True)
            now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(now_time + "  划分完毕\n")


            now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(now_time + "  开始保存训练集raw data：")
            self.txt_write_obj.list_to_txt(data_list = trainData_raw_list, filename_write = "raw_data_train.txt", separator = "\n")

            now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(now_time + "  开始保存测试集raw data：")
            self.txt_write_obj.list_to_txt(data_list = testData_raw_list, filename_write = "raw_data_test.txt", separator = "\n")
            now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(now_time + "  保存完毕\n")


            now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(now_time + "  标签模式：", ", ".join(tag_mode_list))
            print(now_time + "  开始转换为CRF++标准数据集——train：")

            for i in range(len(tag_mode_list)):

                trainData_list = self.data_raw_to_CRF(data_raw_list = trainData_raw_list, create_mode_dict = create_mode_dict, separator_for_tags = separator_for_tags, tag_mode = tag_mode_list[i])
                self.txt_write_obj.list_to_txt(data_list = trainData_list, filename_write = "train_" + tag_mode_list[i] + ".txt", separator = "\n")

            now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(now_time + "  开始转换为CRF++标准数据集——test：")

            for i in range(len(tag_mode_list)):

                testData_list = self.data_raw_to_CRF(data_raw_list = testData_raw_list, create_mode_dict = create_mode_dict, separator_for_tags = separator_for_tags, tag_mode = tag_mode_list[i])
                self.txt_write_obj.list_to_txt(data_list = testData_list, filename_write = "test_" + tag_mode_list[i] + ".txt", separator = "\n")

            now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(now_time + "  转换完毕\n")

        elif test_size == 0:

            now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(now_time + "  标签模式：", ", ".join(tag_mode_list))
            print(now_time + "  开始转换为CRF++标准数据集——train：")

            for i in range(len(tag_mode_list)):

                trainData_list = self.data_raw_to_CRF(data_raw_list = trainData_raw_list, create_mode_dict = create_mode_dict, separator_for_tags = separator_for_tags, tag_mode = tag_mode_list[i])
                self.txt_write_obj.list_to_txt(data_list = trainData_list, filename_write = "train_" + tag_mode_list[i] + ".txt", separator = "\n")

            now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(now_time + "  转换完毕\n")

        elif test_size == 1:

            now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(now_time + "  开始转换为CRF++标准数据集——test：")

            for i in range(len(tag_mode_list)):

                testData_list = self.data_raw_to_CRF(data_raw_list = testData_raw_list, create_mode_dict = create_mode_dict, separator_for_tags = separator_for_tags, tag_mode = tag_mode_list[i])
                self.txt_write_obj.list_to_txt(data_list = testData_list, filename_write = "test_" + tag_mode_list[i] + ".txt", separator = "\n")

            now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(now_time + "  转换完毕\n")
