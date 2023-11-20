from client.blockchain_client import *
from model.block import *
from typing import Dict


class BlockStats:

    def __init__(self):
        self.block_map: Dict[int, Block] = {}
        self.block_height = 0

    def get_last_block(self):
        """
            获取最新的block信息
        """
        last_block = get_latest_block()
        block = Block(last_block['height'], last_block['time'], last_block['block_index'], last_block['hash'])
        self.block_map[block.height] = block
        self.block_height = last_block['height']
        return block

    def build_blocks_info(self):
        """
            构建最近的区块信息
        """
        blocks = get_one_day_blocks()
        if blocks is not None:
            for item in blocks:
                block = Block(item['height'], item['time'], item['block_index'], item['hash'])
                self.block_map[item['height']] = block
        else:
            print("WARN: get blocks info error")

    def get_block_stats_time(self, number: int = 6):
        """
            获取最近number个区块的统计时间, 要保证区块的连续性
            :return (max_time, avg_time, min_time)
        """
        current_block = self.block_map[self.block_height]
        mined_time_list = []
        current_block_number = current_block.height
        pre_block = self.block_map[current_block_number - 1]
        for _ in range(number):
            mined_time = current_block.time - pre_block.time
            mined_time_list.append(mined_time)
            current_block_number -= 1
            current_block = self.block_map[current_block_number]
            pre_block = self.block_map[current_block_number - 1]

        max_time = max(mined_time_list)
        min_time = min(mined_time_list)
        avg_time = sum(mined_time_list) / len(mined_time_list)
        return max_time, avg_time, min_time
