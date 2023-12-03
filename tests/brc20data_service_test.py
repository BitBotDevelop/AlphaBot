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


if __name__ == '__main__':
    get_minting_rank_test()
