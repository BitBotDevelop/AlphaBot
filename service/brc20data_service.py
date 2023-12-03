from client.brc20data_client import *
from typing import Dict, Any
from model.mint_rank import *


class Brc20Data:
    """
        brc20是数据接口
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def get_minting_rank(self, top_n: int = 10):
        """
            查询mint中的brc20列表, 默认展示top10
        """
        period = "1D"
        # period values: 1b: 最新的1个block, 3b, 10b; 1D: 最近的一天 3D 7D
        if self.config.get('MINT_PERIOD') is not None:
            period = self.config.get('MINT_PERIOD')
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
                if (int(mint_mem_pool) + int(minted_count)) / int(max_supply) >= 1:
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
