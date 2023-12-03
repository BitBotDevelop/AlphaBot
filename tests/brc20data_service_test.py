from service.brc20data_service import *
import os
import json
import jsonpickle

config = {}
brc20_data = Brc20Data(config)


def get_minting_rank_test():
    mint_rank_data = brc20_data.get_minting_rank()

    print("mint_rank_data")
    print(jsonpickle.encode(mint_rank_data))


def get_tick_info_test():
    tick = "mice"
    tick_info = brc20_data.get_tick_info(tick)
    print(jsonpickle.encode(tick_info))


def get_brc20_block_signals_test():
    op = 1
    data = brc20_data.get_brc20_block_signals(op)
    print(jsonpickle.encode(data))


def get_brc20_signals_stats_test():
    op = 1
    data = brc20_data.get_brc20_signals_stats(op)
    print(jsonpickle.encode(data))


if __name__ == '__main__':
    get_minting_rank_test()
