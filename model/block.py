"""
    区块模型
    :param height: 区块高度
    :param time: 区块生成时间
    :param block_index: 区块索引
    :param block_hash: 区块hash
"""


class Block:

    def __init__(self, height: int, time: int, index: int, block_hash: str):
        self.height = height
        self.time = time
        self.block_index = index
        self.hash = block_hash

    def json(self):
        return {
            "height": self.height,
            "time": self.time,
            "block_index": self.block_index,
            "hash": self.hash
        }
