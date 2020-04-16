from tools.CommonTools import string_cut_off_from_key, clean_the_same, sub_str_list_with_regexp

from getCRFTrainData.DataWithExcel import DataWithExcel_read
from getCRFTrainData.DataWithTxt import DataWithTxt_write
from getCRFTrainData.CreateData import CreateCorpName

from sklearn.model_selection import train_test_split
from tqdm import tqdm

import time





if __name__ == "__main__":

    folder_name_read = "inputData"
    folder_name_write = "outputData"
    folder_name_param = "paramData"
    filename_read = "merckcom.xlsx"
    filename_write = "raw_data_merck.txt"


    data_creator = CreateCorpName(folder_name_read = folder_name_read, folder_name_write = folder_name_write, folder_name_param = folder_name_param)
    data_df = data_creator.excel_read_obj.get_data(filename_read = filename_read, return_type = "df", with_title = True, with_index = False)

    data_name_raw_list = list(data_df["name"])
    data_label_raw_list = list(data_df["type"])
    data_name_raw_list = sub_str_list_with_regexp(str_list = data_name_raw_list, regexp = "\(", target = "（")
    data_name_raw_list = sub_str_list_with_regexp(str_list = data_name_raw_list, regexp = "\)", target = "）")
    data_name_raw_list = sub_str_list_with_regexp(str_list = data_name_raw_list, regexp = "\s", target = "")

    ndata = len(data_name_raw_list)

    raw_data_list = ["" for i in range(ndata)]

    for i in tqdm(range(ndata), ncols = 75):
        
        if data_name_raw_list[i][0] == "*" or data_name_raw_list[i][0] == "#":

            data_name_raw_list[i] = data_name_raw_list[i][1 :]

        if data_name_raw_list[i][0] == "（":

            data_name_raw_list[i], _ = string_cut_off_from_key(string = data_name_raw_list[i], key = "）", appear_type = "first", cut_type = "before", include = True)

        if data_name_raw_list[i][-1] == "）":

            data_name_raw_list[i], _ = string_cut_off_from_key(string = data_name_raw_list[i], key = "（", appear_type = "last", cut_type = "after", include = True)

        raw_data_list[i] = data_name_raw_list[i] + "|" + data_label_raw_list[i]

    raw_data_list, _ = clean_the_same(data_list = raw_data_list, orig_sort = True)
    #data_creator.txt_write_obj.list_to_txt(data_list = raw_data_list, filename_write = filename_write, separator = "\n")

    trainData_raw_list, testData_raw_list = train_test_split(raw_data_list, test_size = 0.1, random_state = int(time.time()), shuffle = True)
    trainData_raw_list, devData_raw_list = train_test_split(trainData_raw_list, test_size = 0.1 / 0.9, random_state = int(time.time()), shuffle = True)

    data_creator.txt_write_obj.list_to_txt(data_list = trainData_raw_list, filename_write = "raw_data_train_merck.txt", separator = "\n")
    data_creator.txt_write_obj.list_to_txt(data_list = devData_raw_list, filename_write = "raw_data_dev_merck.txt", separator = "\n")
    data_creator.txt_write_obj.list_to_txt(data_list = testData_raw_list, filename_write = "raw_data_test_merck.txt", separator = "\n")
