from getCRFTrainData.DataWithExcel import DataWithExcel_read




class KeywordManager():

    def __init__(self, folder_name_read):

        self.keyword_read_obj = DataWithExcel_read(folder_name_read = folder_name_read)
        self.lawtype_keyword_matrix = []  # 企业lawtype类型


    # 从文件中读取企业lawtype类型
    # 文件名记得带后缀
    # 下面类似
    def get_keyword_lawtype(self, filename_read):  

        self.lawtype_keyword_matrix = self.keyword_read_obj.get_data(filename_read = filename_read, return_type = "list", with_title = False, with_index = False)
