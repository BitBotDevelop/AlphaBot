from pydantic import BaseModel

'''
    订单模型
    :param order_id: 订单id
    :receive_address: 铭文接收地址
    :pay_from_address: 发起付款的地址
    :pay_to_address: 付款的目标地址
    :amount: 付款金额
    :status: 订单状态
    :conext: 其他上下文信息, json
'''
class Order(BaseModel):
    order_id: int
    receive_address: str
    pay_from_address: str
    pay_to_address: str
    amount: int
    status: str
    context: str
    