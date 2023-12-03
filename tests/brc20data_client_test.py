from client.brc20data_client import *
import os
import json

def get_brc20_ticks_test():
    brc20_list = get_brc20_list()
    json_data = json.dumps(brc20_list)
    with open('brc20_list.json', 'w') as f:
        f.write(json_data)

def get_brc20_mint_rank_test():
    brc20_rank = get_brc20_mint_rank()
    print(brc20_rank)


if __name__ == '__main__':
    get_brc20_mint_rank_test()
