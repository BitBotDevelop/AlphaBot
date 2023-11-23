from client.blockchain_client import *
from client.ordinals_client import *
from client.wallet_client import *
from common.fee_type_enum import FeeType
from typing import Dict, Any
from common.common import *


class BidStrategy:
    """
        出价策略，根据当前网络的gas费，地板价来进行出价
            gas_fee:fastestFee、halfHourFee、hourFee、economyFee、minimumFee
        floor_price: bitmap的地板价
    """

    def __init__(self, wallet: WalletClient, config: Dict[str, Any]):
        self.wallet = wallet
        self.config = config

    def get_fee(self, filename, fee_type: FeeType):
        """
            根据fee_type来获取费率
        """
        if fee_type == FeeType.FLOOR_PRICE:
            # 获取地板价
            floor_price = query_bitmap_floor_price()
            if floor_price > 0:
                return floor_price
            else:
                return get_gas_fee(FeeType.FASTEST_FEE.value)
        else:
            # 根据费用评估结果来决策
            gas_fee = get_gas_fee(fee_type.value)
            floor_price = query_bitmap_floor_price()
            if self.estimate(filename, floor_price, gas_fee):
                return gas_fee
            else:
                # 评估费用过高，则返回0
                return 0

    def estimate(self, filename, floor_price, gas_fee):
        # 如果不进行费用评估，则直接跳过，否则根据评估的费用来选择是否进行下单
        if not self.config[ESTIMATE_FEE]:
            return True
        receive_address = self.wallet.get_unsed_t2pr_address()
        total_fee = inscribe_estimate(receive_address, gas_fee, filename)
        print("estimate ,filename:{}, fast_gas_fee:{}, estimate_total_fee:{}, bitmap floor_price:{}"
              .format(filename, gas_fee, total_fee, floor_price))
        if total_fee >= floor_price:
            print("warning: total fee is greater than floor_price")
            return False
        else:
            return True

