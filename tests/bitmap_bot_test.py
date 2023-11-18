from service.bitmap_bot import *
from client.wallet_client import *


api_keys = ["ecce7b6848238930e191cddc0a8bc9fcb6b442a0fe0248dbab175a85794b548d"]

wallet = WalletClient()
bitmap_bot = BitMapBot(api_keys, wallet)


def run_test():
    bitmap_bot.run()
    
run_test()