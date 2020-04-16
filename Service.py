from BERT_BiLSTM_CRF_master.Config import Config

from BERT_BiLSTM_CRF_master.bert_base.client import BertClient

from tools.CommonTools import timer


import datetime
import time
import os

#import codecs
#import pickle





class NERserviceManager():

    def __init__(self, ip = "127.0.0.1"):

        self.connect_ip = ip
        self.cfg = Config()
        self.cfg.load_config_as_json(mode = "server")
        self.project_folder_path = ""
        self.ner_model_dir = ""
        self.__set_basic_config()
        self.NERclient = None


    def start_NERclient(self):

        self.NERclient = BertClient(ip = self.connect_ip, ner_model_dir = self.ner_model_dir, show_server_config = False, check_version = False, check_length = False, mode = "NER")


    # raw输出结果转化为tuple list
    # NERresult_single是bert client encode方法输出的单个字段的字符列表，格式为["O", "O", "B-LOC"]之类
    @staticmethod
    def get_NER_tag_single(text_single, NERresult_single):

        text_len = len(text_single)
        result_tuple_list = []

        if text_len == 0:

            return result_tuple_list

        else:

            start_index_temp = 0
            end_index_temp = 0
            next_change_NERtype_flag = 1

            for index in range(len(NERresult_single)):

                present_tag_list = NERresult_single[index].split("-")
                present_Wordtype = present_tag_list[0]
                present_NERtype = present_tag_list[-1]

                if index == len(NERresult_single) - 1:  # 当前字符是最后一个

                    result_tuple_list.append((text_single[start_index_temp :], present_NERtype))  # 收尾
                    
                else:

                    next_tag_list = NERresult_single[index + 1].split("-")
                    next_Wordtype = next_tag_list[0]

                    if next_Wordtype == 'B' or (present_Wordtype != 'O' and next_Wordtype == 'O'):

                        next_change_NERtype_flag = 1

                    else:

                        next_change_NERtype_flag = 0

                    if next_change_NERtype_flag == 1:

                        result_tuple_list.append((text_single[start_index_temp : index + 1], present_NERtype))
                        start_index_temp = index + 1
                        
            return result_tuple_list


    @timer
    def NERservice(self, text, keep_alive = True):

        if type(text) == list:

            text_list = text

        elif type(text) == str:

            text_list = [text]
        
        NERresult_list_raw = self.NERclient.encode(text_list)
        NERresult_list = []

        for index in range(len(text_list)):

            NERresult_list.append(self.get_NER_tag_single(text_single = text_list[index], NERresult_single = NERresult_list_raw[index]))

        if keep_alive == False:

            self.stop_NERclient()

        return NERresult_list


    def stop_NERclient(self):

        self.NERclient.close()


    def __set_basic_config(self):

        if os.name == 'nt':

            self.project_folder_path = "\\".join(os.path.abspath(__file__).split("\\")[: -1])
            self.ner_model_dir = self.project_folder_path + "\\models\\BERT-BiLSTM-CRF"

        else:

            self.project_folder_path = "/".join(os.path.abspath(__file__).split("/")[: -1])
            self.ner_model_dir = self.project_folder_path + "/models/BERT-BiLSTM-CRF"




if __name__ == "__main__":

    NERserviceManager_obj = NERserviceManager()
    NERserviceManager_obj.start_NERclient()
    result_tuple_list = NERserviceManager_obj.NERservice(text = "宜兴市中超利永紫砂陶有限公司", keep_alive = False)
    print(result_tuple_list)
    #NERserviceManager_obj.NERservice(text = ["上海见知数据科技上海有限公司" for index in range(1000)], keep_alive = False)
    #label_list = ["O", "B-GEO", "I-GEO", "B-UNN", "I-UNN", "B-BUS", "I-BUS", "B-LAT", "I-LAT", "X", "[CLS]", "[SEP]"]
    #output_dir = r"C:\Users\zihen\Desktop\BERT-BiLSTM-CRF-NER-test\BERT-BiLSTM-CRF-NER-test\BERT-BiLSTM-CRF-NER-test\inputData\formal_training\output"
    #with codecs.open(os.path.join(output_dir, 'label_list.pkl'), 'wb') as rf:
        #pickle.dump(label_list, rf)
