from enum import Enum


class FeeType(Enum):
    FLOOR_PRICE = "floorPrice"
    FASTEST_FEE = "fastestFee"
    HALF_HOUR_FEE = "halfHourFee"
    HOUR_FEE = "hourFee"
    ECONOMY_FEE = "economyFee"
    MINIMUM_FEE = "minimumFee"


def get_fee_type(fee_type_name):
    for fee_type in FeeType:
        if fee_type.name == fee_type_name:
            return fee_type
    raise ValueError(f"Invalid color: {fee_type_name}")