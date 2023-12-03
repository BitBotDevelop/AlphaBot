from client.brc20data_client import *
from typing import Dict, Any
from model.mint_rank import *


class Brc20Data:
    """
        brc20是数据接口
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def get_minting_rank(self, top_n: int = 10, period: str = "1D"):
        """
            查询mint中的brc20列表, 默认展示top10
        """
        # period values: 1b: 最新的1个block, 3b, 10b; 1D: 最近的一天 3D 7D
        mint_rank = get_brc20_mint_rank(api_key=self.config.get("API_KEY"), period=period)
        mint_rank_rs = []
        if mint_rank is not None:
            rows = mint_rank['rows']
            minted = mint_rank['minted']
            for item in rows:
                inscription_id = item['inscriptionId']
                mints = item['mints']
                tick = item['tick']
                tick_detail = minted[inscription_id]
                max_supply = tick_detail['max']
                holders = tick_detail['holders']
                minted_count = tick_detail['minted']
                mint_mem_pool = tick_detail['mintMemPool']
                # 去除已经mint完成的tick
                if (float(mint_mem_pool) + float(minted_count)) / float(max_supply) >= 1:
                    print('the tick:{} has minted over'.format(tick))
                    continue
                mint_rank_model = MintRankModel(inscription_id=inscription_id, tick=tick,
                                                mints=mints, holders=holders, max_supply=max_supply,
                                                minted=minted_count, mint_mem_pool=mint_mem_pool)

                mint_rank_rs.append(mint_rank_model)

        mint_rank_sorted = sorted(mint_rank_rs)
        return mint_rank_sorted[: top_n]

    def get_tick_info(self, tick):
        return get_brc20_tick_info(api_key=self.config.get("API_KEY"), tick=tick)

    def get_brc20_block_signals(self, op: int):
        """
            获取brc20每个区块的信号
        """
        brc20_signals = get_brc20_alpha_signals(api_key=self.config.get("API_KEY"), op=op)
        block_signal_dict = {}
        for block_item in brc20_signals:
            block_number = block_item['blockNumber']
            tick_signal_dict = {}
            for tx in block_item['list']:
                if str(tx['p']) != 'brc20':
                    continue
                tick = tx['tick']
                if tick not in tick_signal_dict.keys():
                    brc20_signal = Brc20SignalDetailModel(tick)
                    tick_signal_dict[tick] = brc20_signal
                tick_signal_dict[tick].add(tx['address'], int(tx['amount']))
            block_signal_dict[block_number] = tick_signal_dict

        return block_signal_dict

    def get_brc20_signals_stats(self, op: int):
        """
            获取brc20多个区块的统计信号
        """
        brc20_signals = get_brc20_alpha_signals(api_key=self.config.get("API_KEY"), op=op)
        brc20_signals_stats = {}
        tick_signal_dict = {}
        block_numbers = {}
        for block_item in brc20_signals:
            block_numbers[block_item['blockNumber']] = block_item['time']
            for tx in block_item['list']:
                if str(tx['p']) != 'brc20':
                    continue
                tick = tx['tick']
                if tick not in tick_signal_dict.keys():
                    brc20_signal = Brc20SignalDetailModel(tick)
                    tick_signal_dict[tick] = brc20_signal
                tick_signal_dict[tick].add(tx['address'], float(tx['amount']))

        brc20_signals_stats['block_numbers'] = block_numbers
        brc20_signals_stats['tick_signal_dict'] = tick_signal_dict
        return brc20_signals_stats
