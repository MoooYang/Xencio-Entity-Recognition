from BERT_BiLSTM_CRF_master.bert_base.runs import start_server

from BERT_BiLSTM_CRF_master.Config import Config


def stop_NERserver(NERserver):

    NERserver.close()



if __name__ == "__main__":

    cfg = Config()
    cfg.load_config_as_json(mode = "server")
    cfg.change_one_in_config(name = "cpu", value = True)  # 使得cpu为默认设备


    NERserver = start_server(cfg = cfg)
    NERserver.start()
    NERserver.join()
