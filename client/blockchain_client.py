import requests
import json

def get_latest_block_number():
    '''
        查询最新的区块高度
    '''
    url = "https://blockchain.info/latestblock"
    print("query latest block number, url:{}".format(url))
    
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print("ERROR call blockchain api to query latest block number error")
            return -1
        print("response:", response.text)
        return json.loads(response.text)['height']
    except Exception as e:
        print("call blockchain api to query latest block number error, message:", e)
        return 0

def get_gas_detail():
    '''
        获取当前btc网络的gas费
        返回值：
        {
            "fastestFee": 343,
            "halfHourFee": 319,
            "hourFee": 299,
            "economyFee": 46,
            "minimumFee": 23
        }
    '''
    url = "https://mempool.space/api/v1/fees/recommended"
    try:
        response = requests.get(url)
        print("response:", response)
        return response
    except Exception as e:
        print("call mempool api to get gas recommend error", e)
        return None
    

def get_gas_fee(type="halfHourFee"):
    '''
        根据指定类型获取当前网络的gas费
    '''
    gas_detail = get_gas_detail()
    print("gas_detail:", gas_detail)
    if gas_detail is not None:
        return gas_detail[type]
    else:
        return 0
    