"""
    mint 排名
    min progress = (minted +mint_mem_pool)/max_supply
"""


class MintRankModel:
    def __init__(self, inscription_id: str, tick: str, mints: int, holders: int, max_supply: int, minted: int,
                 mint_mem_pool: int):
        self.inscription_id = inscription_id
        self.tick = tick
        self.mints = mints
        self.holders = holders
        self.max_supply = max_supply
        self.minted = minted
        self.mint_mem_pool = mint_mem_pool
        self.mint_progress = round((int(self.minted) + int(self.mint_mem_pool))/int(self.max_supply) * 100, 2)

    def __lt__(self, other):
        return self.mint_progress > other.mint_progress
