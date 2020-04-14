import pandas as pd
import numpy as np
import fool

import datetime
import copy
import time
import re




# 用于计时的修饰器
def timer(function):

    def count_time(*args, **kwargs):

        start_time = time.time()
        result = function(*args, **kwargs)
        end_time = time.time()

        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(now_time + "  耗时：%.2f秒\n" %(end_time - start_time))
        
        return result

    return count_time


# 去重，并保留原来的顺序
# 要求输入一个list，返回去重后的列表及元素数量
def clean_the_same(data_list, orig_sort = True):

    new_data_list = list(set(data_list))  # 去重

    if orig_sort == True:

        new_data_list.sort(key = data_list.index)  # 按原来顺序排列

    return new_data_list, len(new_data_list)


# 给定一个字符串list，把每个字符根据某个正则表达式替换成对应的内容
def sub_str_list_with_regexp(str_list, regexp, target = ""):

    str_list = [re.sub(regexp, target, string) for string in str_list]

    return str_list


# 判断一个string里是否包含一个矩阵里的关键字
# 行指标越小，越先进行查找
# 同一行里，列指标越小，越先进行查找
# keyword matrix是一个嵌套list，方形，每行末尾不足的地方用""填充
# 返回判断和对应的关键字，以及对应keyword matrix中的位置，未搜索到时为 -1， -1
# 因为是find方法，所以只查第一个keyword
def keyword_matrix_in_word(keyword_matrix, string):

    nrows = len(keyword_matrix)
    ncols = len(keyword_matrix[0])

    for row_index in range(nrows):

        col_index = 0

        while (col_index < ncols) and (keyword_matrix[row_index][col_index] != ""):

            if string.find(keyword_matrix[row_index][col_index]) != -1:

                return [True, keyword_matrix[row_index][col_index], row_index, col_index]

            else:

                col_index += 1

    return [False, "", -1, -1]


# 查找关键字的位置
# first代表第第一次出现该关键字的位置，last表示最后一次
# -1则表示不存在
def string_find_key_index(string, key, appear_type = "first"):

    index_temp = string.find(key)

    if appear_type == "first":

        return index_temp

    elif appear_type == "last":

        if index_temp == -1:

            return -1

        elif index_temp + len(key) < len(string):  # 第一个key之后还有剩余字段的话

            string_next = string[index_temp + len(key) :]  
            index_next = string_find_key_index(string = string_next, key = key, appear_type = "last")

            if index_next != -1:

                return index_temp + len(key) + index_next

            else:

                return index_temp

        else:

            return index_temp


# 给定一个字符串，根据关键字及位置舍弃字符串
# 例：关键字为"银行"，"中国工商银行上海分行"→"中国工商银行"
# include表示是否把该关键字也去掉
# appear_type表示key第几次出现，只可以是first或last
def string_cut_off_from_key(string, key, appear_type = "first", cut_type = "after", include = False):

    key_index = string_find_key_index(string = string, key = key, appear_type = appear_type)  # 寻找key

    if key_index == -1:

        return string, key_index

    else:
        
        if cut_type == "after":

            if include == True:

                return string[: key_index], key_index

            else:

                if key_index + len(key) < len(string):  # 关键词不是最后一个词

                    return string[: key_index + len(key)], key_index

                else:

                    return string, key_index

        else:

            if include == False:

                return string[key_index :], key_index

            else:

                if key_index + len(key) < len(string):

                    return string[key_index + len(key) :], key_index

                else:

                    return "", key_index


# 把类似[("xxx", 1), ("yyy", 2)]这样的元组列表，按某个位置的字符合并为字符串
def merge_tuple_list(tuple_list, axis):

    list_to_merge = [str(tuple_list[i][axis]) for i in range(len(tuple_list))]

    return "".join(list_to_merge)


# 在类似[("xxx", 1), ("yyy", 2)]这样的元组列表中，根据axis，搜索关键词的位置
def tuple_list_find_key_index(tuple_list, axis, key, appear_type = "first"):

    index_temp = -1
    count = 0

    if appear_type == "first":

        for tup in tuple_list:

            if tup[axis] == key:

                index_temp = count
                return index_temp

            else:

                count += 1

        return -1

    elif appear_type == "last":

        for tup in tuple_list:

            if tup[axis] == key:

                index_temp = count

            count += 1

        return index_temp


# 从一维列表中抽样，replace为False代表无放回
def sample_from_list(n, data_list, replace = False):

    data_df = pd.DataFrame(data = data_list)

    sample_list = list(data_df.sample(n = n, replace = False, random_state = int(time.time()))[0])

    return sample_list
