# -*- coding: utf-8 -*-

"""

 @Time    : 2019/1/30 16:47
 @Author  : MaCan (ma_cancan@163.com)
 @File    : __init__.py.py
"""

from ...Config import Config


def start_server(cfg):
    from ..server import BertServer
    from ..server.helper import get_run_args

    args = get_run_args(cfg = cfg)
    # print(args)
    server = BertServer(args)

    return server


def start_client():
    pass


# cfg : Config obj
def train_ner(cfg, customer_label_list = []):
    import os
    from ..train.train_helper import get_args_parser
    from ..train.bert_lstm_ner import train


    args = get_args_parser(cfg = cfg)
    if True:
        import sys
        param_str = '\n'.join(['%20s = %s' % (k, v) for k, v in sorted(vars(args).items())])
        print('usage: %s\n%20s   %s\n%s\n%s\n' % (' '.join(sys.argv), 'ARG', 'VALUE', '_' * 50, param_str))
    # print(args)
    os.environ['CUDA_VISIBLE_DEVICES'] = args.device_map
    train(args=args, customer_label_list = customer_label_list)

# if __name__ == '__main__':
#     # start_server()
#     train_ner()