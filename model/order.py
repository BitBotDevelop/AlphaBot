"""
    订单模型
    :param order_id: 订单id
    :receive_address: 铭文接收地址
    :pay_from_address: 发起付款的地址
    :pay_to_address: 付款的目标地址
    :amount: 付款金额
    :order_status: 订单状态
    :context: 其他上下文信息, json
"""


class Order:

    def __init__(self, order_id: int, receive_address: str, pay_from_address: str, pay_to_address: str, amount: int,
                 order_status: str, context: str):
        self.order_id = order_id
        self.receive_address = receive_address
        self.pay_from_address = pay_from_address
        self.pay_to_address = pay_to_address
        self.amount = amount
        self.order_status = order_status
        self.context = context
