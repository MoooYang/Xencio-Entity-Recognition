import os




class DataBase():

    def __init__(self, folder_name_work):

        self.project_folder_path = "\\".join(os.path.abspath(__file__).split("\\")[: -2])
        self.folder_path_work= self.project_folder_path + "\\" + folder_name_work  # 工作文件夹的绝对路径
