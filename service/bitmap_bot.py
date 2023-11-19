from client.blockchain_client import *
from client.ordinals_client import *
from client.unisat_client import *
from client.wallet_client import *
from typing import List
import random


class BitMapBot:

    def __init__(self, api_keys: List[str], wallet: WalletClient) -> None:
        self.api_keys = api_keys
        self.wallet = wallet

    def get_api_key(self):
        if self.api_keys is None or len(self.api_keys):
            return "ecce7b6848238930e191cddc0a8bc9fcb6b442a0fe0248dbab175a85794b548d"
        else:
            return random.choice(self.api_keys)

    def run(self):
        # 1 查询当前最新的区块
        block_height = get_latest_block_number()
        if block_height <= 0:
            print("error, get block height error, wait to re run")
            return
        # 2 评估是否需要创建一个交易订单
        filename = str(block_height) + ".bitmap"
        # 3 获取当前网络的gas费用
        gas_fee = get_gas_fee("fastestFee")
        receive_address = self.wallet.get_unsed_t2pr_address()
        total_fee = inscribe_estimate(receive_address, gas_fee, filename)
        # 4 获取当前bitmap的地板价
        floor_price = query_bitmap_floor_price()
        print("estimate order,filename:{}, fast_gas_fee:{}, estimate_total_fee:{}, bitmap floor_price:{}"
              .format(filename, gas_fee, total_fee, floor_price))
        if total_fee >= floor_price:
            print("warning: total fee is greater than floor_price")

        # 5 获取一个bitmap的接收地址
        receive_address = self.wallet.get_unsed_t2pr_address()
        dev_address = self.wallet.get_dev_address()
        (order_id, amount, pay_address) = create_order(self.get_api_key(), filename, receive_address, gas_fee, dev_address)
        # 6 对订单进行支付
        self.wallet.pay_for_order(order_id, amount, pay_address, receive_address)
        # 7 等待unisat提交交易到链上，后续订单交易监控由单独的线程处理


def main():
    pass


if __name__ == "__main__":
    main()
