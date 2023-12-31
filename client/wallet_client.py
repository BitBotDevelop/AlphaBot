"""
对钱包相关的操作，包括生成新的taproot地址，以及对订单进行付款
"""


class WalletClient:

    def __init__(self) -> None:
        pass

    def get_unsed_t2pr_address(self):
        """
            从数据库或者直接生成一个可用的taproot地址
        """
        return "bc1plgwatah04qpmw66lmclr6vk6ay5qvnx42kv3xmyn8rcn6j2jcwasv8w3vm"

    def get_dev_address(self):
        """
            获取开发者地址来接收额外的费用
        """
        return "bc1pv8e6fx8yvjh0rj3m87su4gfff0arrg8nhjxhpkjslnztwc47rvqsdhtl3v"

    def pay_for_order(self, order_id: int, amount: int, pay_address: str, receive_address: str, status: str):
        """
            对订单进行付款，并保存到数据库中, 通过消息队列发送到订单监控线程以查询订单的状态
        """
        print("pay for the order,order_id:{},amount:{}, pay_to_address:{},receive_address:{}, order status:{}"
              .format(order_id, amount, pay_address, receive_address, status))
