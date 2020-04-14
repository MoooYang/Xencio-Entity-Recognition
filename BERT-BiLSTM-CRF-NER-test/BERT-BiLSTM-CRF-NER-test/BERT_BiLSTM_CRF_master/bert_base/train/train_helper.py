# -*- coding: utf-8 -*-

"""

 @Time    : 2019/1/30 14:01
 @Author  : MaCan (ma_cancan@163.com)
 @File    : train_helper.py
"""

import argparse
import os

__all__ = ['get_args_parser']




def get_args_parser(cfg):
    from .bert_lstm_ner import __version__
    parser = argparse.ArgumentParser()

    if os.name == 'nt':
        # 修改，获取项目地址
        project_folder_path = "\\".join(os.path.abspath(__file__).split("\\")[: -4])
        bert_path = project_folder_path + "\\models\\bert\\chinese_L-12_H-768_A-12"
        root_path = project_folder_path + "\\inputData\\formal_training"
    else:
        project_folder_path = "/".join(os.path.abspath(__file__).split("/")[: -4])
        bert_path = project_folder_path + "/models/bert/chinese_L-12_H-768_A-12"
        root_path = project_folder_path + "/inputData/formal_training"
        
    param_dict = cfg.config_dict

    group1 = parser.add_argument_group('File Paths',
                                       'config the path, checkpoint and filename of a pretrained/fine-tuned BERT model')
    group1.add_argument('-data_dir', type=str, default=os.path.join(root_path, "NERdata" + "_" + param_dict["tag_mode"]),
                        help='train, dev and test data dir')
    group1.add_argument('-bert_config_file', type=str, default=os.path.join(bert_path, 'bert_config.json'))
    group1.add_argument('-output_dir', type=str, default=os.path.join(root_path, 'output'),
                        help='directory of a pretrained BERT model')
    group1.add_argument('-init_checkpoint', type=str, default=os.path.join(bert_path, 'bert_model.ckpt'),
                        help='Initial checkpoint (usually from a pre-trained BERT model).')
    group1.add_argument('-vocab_file', type=str, default=os.path.join(bert_path, 'vocab.txt'),
                        help='')

    group2 = parser.add_argument_group('Model Config', 'config the model params')
    group2.add_argument('-max_seq_length', type=int, default=param_dict["max_seq_length"],  # 默认202
                        help='The maximum total input sequence length after WordPiece tokenization.')
    group2.add_argument('-do_train', action='store_false', default=param_dict["do_train"],
                        help='Whether to run training.')
    group2.add_argument('-do_eval', action='store_false', default=param_dict["do_eval"],
                        help='Whether to run eval on the dev set.')
    group2.add_argument('-do_predict', action='store_false', default=param_dict["do_predict"],
                        help='Whether to run the predict in inference mode on the test set.')
    group2.add_argument('-batch_size', type=int, default=param_dict["batch_size"],  # 默认64
                        help='Total batch size for training, eval and predict.')
    group2.add_argument('-learning_rate', type=float, default=param_dict["learning_rate"],  # 默认1e-5
                        help='The initial learning rate for Adam.')
    group2.add_argument('-num_train_epochs', type=float, default=param_dict["num_train_epochs"],  # 默认10
                        help='Total number of training epochs to perform.')
    group2.add_argument('-dropout_rate', type=float, default=param_dict["dropout_rate"],
                        help='Dropout rate')
    group2.add_argument('-clip', type=float, default=param_dict["clip"],
                        help='Gradient clip')
    group2.add_argument('-warmup_proportion', type=float, default=param_dict["warmup_proportion"],
                        help='Proportion of training to perform linear learning rate warmup for '
                             'E.g., 0.1 = 10% of training.')
    group2.add_argument('-lstm_size', type=int, default=param_dict["lstm_size"],
                        help='size of lstm units.')
    group2.add_argument('-num_layers', type=int, default=param_dict["num_layers"],
                        help='number of rnn layers, default is 1.')
    group2.add_argument('-cell', type=str, default=param_dict["cell"],
                        help='which rnn cell used.')
    group2.add_argument('-save_checkpoints_steps', type=int, default=param_dict["save_checkpoints_steps"],
                        help='save_checkpoints_steps')
    group2.add_argument('-save_summary_steps', type=int, default=param_dict["save_summary_steps"], 
                        help='save_summary_steps.')
    group2.add_argument('-filter_adam_var', type=bool, default=False,
                        help='after training do filter Adam params from model and save no Adam params model in file.')
    group2.add_argument('-do_lower_case', type=bool, default=True,
                        help='Whether to lower case the input text.')
    group2.add_argument('-clean', type=bool, default=param_dict["clean"])
    group2.add_argument('-device_map', type=str, default=param_dict["device_map"],
                        help='witch device using to train')

    # add labels
    group2.add_argument('-label_list', type=str, default=None,
                        help='User define labels， can be a file with one label one line or a string using \',\' split')

    parser.add_argument('-verbose', action='store_true', default=param_dict["verbose"],
                        help='turn on tensorflow logging for debug')
    parser.add_argument('-ner', type=str, default='ner', help='which modle to train')
    parser.add_argument('-version', action='version', version='%(prog)s ' + __version__)
    return parser.parse_args()
