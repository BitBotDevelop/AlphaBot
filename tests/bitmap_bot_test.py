from service.bitmap_bot import *
from client.wallet_client import *
from strategy.bid_strategy import *
from common.common import *
import os

api_keys = ["ecce7b6848238930e191cddc0a8bc9fcb6b442a0fe0248dbab175a85794b548d"]

# 系统配置
config = {FEE_TYPE: FeeType.FASTEST_FEE.name, API_KEYS: api_keys, ESTIMATE_FEE: True}

wallet = WalletClient()
block_stats = BlockStats()
bid_strategy = BidStrategy(wallet, config)
bitmap_bot = BitMapBot(config, wallet, block_stats, bid_strategy)


def run_test():
    block_height = block_stats.get_last_block().height
    bitmap_bot.run(block_height)


run_test()
