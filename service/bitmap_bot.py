from client.ordinals_client import *
from client.unisat_client import *
from client.wallet_client import *
from typing import Dict, Any
from service.block_stats import *
from strategy.bid_strategy import BidStrategy
from common.common import *
from common.fee_type_enum import *
import random


class BitMapBot:

    def __init__(self, config: Dict[str, Any], wallet: WalletClient,
                 block_stats: BlockStats, bid_strategy: BidStrategy) -> None:
        self.config = config
        self.wallet = wallet
        self.block_stats = block_stats
        self.bid_strategy = bid_strategy

    def get_api_key(self):
        if self.config.get(API_KEYS) is None or len(self.config.get(API_KEYS)):
            return "ecce7b6848238930e191cddc0a8bc9fcb6b442a0fe0248dbab175a85794b548d"
        else:
            return random.choice(self.config.get(API_KEYS))

    def run(self, block_height):
        # 1 当前最新的区块
        if block_height <= 0:
            print("error, get block height error, wait to re run")
            return
        # 2 评估是否需要创建一个交易订单
        filename = str(block_height) + ".bitmap"
        # 3 根据出价策略获取出价
        fee_type = get_fee_type(self.config.get(FEE_TYPE))
        bid_fee = self.bid_strategy.get_fee(filename, fee_type)
        if bid_fee <= 0:
            print("this time we will not to send tx,filename:{}".format(filename))
            return

            # 4 获取一个bitmap的接收地址
        receive_address = self.wallet.get_unsed_t2pr_address()
        dev_address = self.wallet.get_dev_address()
        (order_id, amount, pay_address, status) = create_order(self.get_api_key(), filename, receive_address, bid_fee,
                                                               dev_address)
        # 6 对订单进行支付
        self.wallet.pay_for_order(order_id, amount, pay_address, receive_address, status)
        # 7 等待unisat提交交易到链上，后续订单交易监控由单独的线程处理


def main():
    pass


if __name__ == "__main__":
    main()
