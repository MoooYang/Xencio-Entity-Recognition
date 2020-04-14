from getCRFTrainData.CreateData import CreateCorpName
from getCRFTrainData.DataWithTxt import DataWithTxt_read, DataWithTxt_write
from getCRFTrainData.DataWithExcel import DataWithExcel_read
from getCRFTrainData.CreateData import CreateCorpName

from tqdm import tqdm

import copy
import re




folder_name_read = "inputData"
filename_read_txt = "raw_data_merck.txt"
filename_read_excel = "对手方名称源数据清洗与预分类(尚未检索纳税人识别号)_新_全.xlsx"

folder_name_write = "outputData"
filename_write = "businessScope_xencio"
filename_write_txt = "businessScope_xencio.txt"
filename_write_excel = "businessScope_xencio.xlsx"

folder_name_param = "paramData"

txtRead_obj = DataWithTxt_read(folder_name_read = folder_name_read)
txtWrite_obj = DataWithTxt_write(folder_name_write = folder_name_write)
corpName_creator = CreateCorpName(folder_name_read = folder_name_read, folder_name_write = folder_name_write, folder_name_param = folder_name_param)


# 读取原始公司数据并获取经营范围
#corpName_creator.get_businessScope(filename_read = filename_read_excel, filename_write = filename_write)


# 去重
#filename_read_txt = "place.txt"
#corpName_creator.remove_duplicate(filename_read_txt = filename_read_txt, filename_write_txt = filename_read_txt)

'''
from tools.CommonTools import string_cut_off_from_key, clean_the_same
filename_temp = "新疆地区.txt"

data_list = corpName_creator.txt_read_obj.get_data(filename_read = filename_temp, return_type = "list")

data_list = [re.findall(">(.*?)</a>", string = string)[0] for string in data_list]

corpName_creator.txt_write_obj.list_to_txt(data_list = data_list, filename_write = filename_temp, separator = "\n")
'''

# 获取raw训练集
#corpName_creator.get_trainData_raw(place_filename_txt = "place.txt", uniqueName_filename_txt = "uniqueName.txt", \
    #businessScope_filename_txt = "businessScope.txt", lawType_filename_txt = "lawType.txt", \
    #trainData_raw_filename_txt = "raw_data.txt")


# 获取CFR++标准训练集
#trainData_raw_filename_txt = "raw_data.txt"
trainData_raw_filename_txt = "raw_data_merck.txt"
test_size = 0.10
#test_size = 0.05 / 0.95

create_mode_dict = {
    0 : "place",
    1 : "uniqueName",
    2 : "businessScope",
    3 : "lawType"
    }
separator_for_tags = " "
tag_mode_list = ["BIO", "BMEWO"]

#corpName_creator.get_train_test_Data(trainData_raw_filename_txt = trainData_raw_filename_txt, create_mode_dict = create_mode_dict, \
    #test_size = test_size, separator_for_tags = separator_for_tags, tag_mode_list = tag_mode_list)





filename_read = "raw_data_test_merck.txt"
filename_write = "test_merk.txt"

raw_data_list = txtRead_obj.get_data(filename_read = filename_read, return_type = "list")

data_list = []

for raw_data_single in tqdm(raw_data_list, ncols = 75):

    raw_data_single_list = raw_data_single.split("|")

    if raw_data_single_list[1] != "":

        data_single_list = corpName_creator.string_plus_sth_to_list(string = raw_data_single_list[0], tag = raw_data_single_list[1], separator_for_sth = " ", tag_mode = "BIO")
        data_single_list.append("")
        data_list.extend(copy.deepcopy(data_single_list))

txtWrite_obj.list_to_txt(data_list = data_list, filename_write = filename_write, separator = "\n")



