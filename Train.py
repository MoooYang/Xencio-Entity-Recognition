from BERT_BiLSTM_CRF_master.bert_base.runs import train_ner

from BERT_BiLSTM_CRF_master.Config import Config




def train(customer_label_list = []):

    cfg = Config()
    cfg.load_config_as_json(mode = "train")

    #cfg.change_one_in_config(name = "tag_mdde", value = "BMEWO")
    tag_mode = cfg.config_dict["tag_mode"]

    if customer_label_list == []:
        
        if tag_mode == "BIO":

            customer_label_list = ["O", "B-GEO", "I-GEO", "B-UNN", "I-UNN", "B-BUS", "I-BUS", "B-LAT", "I-LAT", "X", "[CLS]", "[SEP]"]
    
        elif tag_mode == "BMEWO":

            customer_label_list = ["O", "B-GEO", "M-GEO", "E-GEO", "B-UNN", "M-UNN", "E-UNN", "B-BUS", "M-BUS", "E-BUS", "B-LAT", "M-LAT", "E-LAT", "X", "[CLS]", "[SEP]"]
        
    train_ner(cfg = cfg, customer_label_list = customer_label_list)