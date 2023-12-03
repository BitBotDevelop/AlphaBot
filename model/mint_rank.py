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
        self.mint_progress = round((float(self.minted) + float(self.mint_mem_pool)) / float(self.max_supply) * 100, 2)

    def __lt__(self, other):
        return self.mint_progress > other.mint_progress


class Brc20SignalDetailModel:
    def __init__(self, tick: str):
        """
            @param tick: tick
        """
        self.tick = tick
        self.amount = 0
        self.addresses = set()
        self.address_number = 0

    def add(self, address: str, amount: float):
        self.amount += amount
        self.addresses.add(address)
        self.address_number = len(self.addresses)


