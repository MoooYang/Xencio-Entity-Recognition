from Train import train

from BERT_BiLSTM_CRF_master.Config import Config



if __name__ == "__main__":

    customer_label_list = ["O", 
                           "B-Chemical", "I-Chemical",
                           "B-Dealer", "I-Dealer",
                           "B-Diagnostic", "I-Diagnostic",
                           "B-Hospital", "I-Hospital",
                           "B-Industrial", "I-Industrial",
                           "B-NonProfit", "I-NonProfit",
                           "B-Pharma", "I-Pharma",
                           "B-Service", "I-Service",
                           "B-University", "I-University",
                           "X", "[CLS]", "[SEP]"
                           ]

    train(customer_label_list = customer_label_list)