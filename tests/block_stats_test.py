from service.block_stats import *

block_stats = BlockStats()

latest_block = block_stats.get_last_block()
print(latest_block.json())

block_stats.build_blocks_info()
for block_number in block_stats.block_map.keys():
    print(block_number, "->", block_stats.block_map[block_number].json())

block_stats_time = block_stats.get_block_stats_time()
print(block_stats_time)
