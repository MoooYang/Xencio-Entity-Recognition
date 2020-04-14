from Service import NERserviceManager
from getCRFTrainData.DataWithExcel import DataWithExcel_read
from getCRFTrainData.DataWithTxt import DataWithTxt_write

import os



if __name__ == "__main__":

    folder_name_read = "inputData"
    folder_name_write = "outputData"
    filename_read = "real_test.xlsx"
    filename_write = "real_test_output.txt"

    excel_reader = DataWithExcel_read(folder_name_read = folder_name_read)
    txt_writer = DataWithTxt_write(folder_name_write = folder_name_write)

    data_list = list(excel_reader.get_data(filename_read = filename_read, return_type = "df", with_title = True, with_index = False)["name"])

    NERserviceManager_obj = NERserviceManager()
    NERserviceManager_obj.start_NERclient()
    result_tuple_list = NERserviceManager_obj.NERservice(text = data_list, keep_alive = False)

    list_to_write = [str(tuple_list_single) for tuple_list_single in result_tuple_list]

    txt_writer.list_to_txt(filename_write = filename_write, data_list = [str(tuple_list_single) for tuple_list_single in result_tuple_list], separator = "\n")
