from base.DataBase import DataBase

import json
import os


class Config(DataBase):

    def __init__(self):

        DataBase.__init__(self, folder_name_work = "paramData")
        self.config_file_path = ""
        self.config_dict = {}


    # 读取配置文件，mode为"train"或者"server", 文件名为train.cfg或者server.cfg
    def load_config_as_json(self, mode):
        
        self.config_file_path = os.path.join(self.folder_path_work, mode + ".cfg")
        
        with open(self.config_file_path, "r") as config_file:
            
            self.config_dict = json.load(config_file)
            
            
    # 写入配置文件
    def write_config_to_json(self, mode):
    
        with open(self.config_file_path, "w") as config_file:
            
            json.dump(self.congfig_dict, congfig_file)
            
            
    # 修改config的一个值
    # name为参数名的string
    def change_one_in_config(self, name, value):
    
        self.config_dict[name] = value