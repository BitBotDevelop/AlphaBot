import client.http_client
import time


def get_latest_block():
    """
        查询最新的区块高度
    """
    url = "https://blockchain.info/latestblock"
    print("query latest block, url:{}".format(url))

    try:
        response = client.http_client.get(url)
        if response is not None:
            return response
        else:
            return 0
    except Exception as e:
        print("call blockchain api to query latest block error, message:", e)
        return 0


def get_one_day_blocks():
    """
        获取一天内的区块详情
        :return
        [
            {
                "hash":"000000000000000000037d949006b5aa937a6da3979c843b24edcb6e3982e1bc",
                "height":817615,
                "time":1700464150,
                "block_index":817615
            }
        ]
    """
    import time
    current_time = int(time.time() * 1000)
    try:
        url = "https://blockchain.info/blocks/{}?format=json".format(current_time)
        response = client.http_client.get(url)
        if response is not None:
            return response
        else:
            return None
    except Exception as e:
        print("call blockchain api to get blocks in last day,message:", e)
        return None


def get_gas_detail():
    """
        获取当前btc网络的gas费
        返回值：
        {
            "fastestFee": 343,
            "halfHourFee": 319,
            "hourFee": 299,
            "economyFee": 46,
            "minimumFee": 23
        }
    """
    url = "https://mempool.space/api/v1/fees/recommended"
    try:
        response = client.http_client.get(url)
        print("response:", response)
        return response
    except Exception as e:
        print("call mempool api to get gas recommend error", e)
        return None


def get_gas_fee(fee_type="halfHourFee"):
    """
        根据指定类型获取当前网络的gas费
    """
    gas_detail = get_gas_detail()
    print("gas_detail:", gas_detail)
    if gas_detail is not None:
        return gas_detail[fee_type]
    else:
        return 0
