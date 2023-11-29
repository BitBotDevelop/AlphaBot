import client.http_client
import time
import requests
import json


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

def broadcast_tx(tx_hex, network="testnet"):
    """
        广播交易到链上，使用blockstream
    """
    net = ""
    if network == "testnet":
        net = "testnet/"
    # 设置基本的 URL
    base_url = "https://blockstream.info/" + net + "api/tx"

    try:
        response = requests.post(base_url, tx_hex)
        return response
    except Exception as e:
        print("call blockchain api to broadcast tx error, message:", e)
        return None
    
def broadcast_tx_v2(tx_hex, network="testnet"):
    """
        广播交易到链上, 使用mempool
    """
    net = ""
    if network == "testnet":
        net = "testnet/"
    # 设置基本的 URL
    base_url = "https://mempool.space/" + net + "api/tx"

    try:
        response = requests.post(base_url, tx_hex)
        print("response:", response)
        return response
    except Exception as e:
        print("call blockchain api to broadcast tx error, message:", e)
        return None

def is_valid_json(data):
    try:
        json.loads(data)
        return True
    except ValueError:
        return False
    
async def address_once_had_money(address, network="testnet"):
    """
        查询地址是否接收到资金
    """
    
    url = f"https://mempool.space/api/address/{address}"
    if network == "testnet":
        url = f"https://mempool.space/testnet/api/address/{address}"
    
    print(url)
    
    try:
        response = requests.get(url)
        nonjson = response.text
        
        if any(error_keyword in nonjson.lower() for error_keyword in ['rpc error', 'too many requests', 'bad request']):
            if network == 'main':
                url = f"https://blockstream.info/api/address/{address}"
                response = requests.get(url)
                nonjson = response.text
    except Exception as e:
        if network == 'main':
            url = f"https://blockstream.info/api/address/{address}"
            response = requests.get(url)
            nonjson = response.text

    print("response:", nonjson)
    if not is_valid_json(nonjson):
        return False
    
    json_data = json.loads(nonjson)
    
    if json_data["chain_stats"]["tx_count"] > 0 or (json_data["mempool_stats"]["tx_count"] > 0):
        return True
    
    return False

async def address_received_money_in_this_tx(address: str,  network="testnet"):
    """
        查询地址是否接收到资金
    """

    url = f"https://mempool.space/api/address/{address}/txs"
    if network == "testnet":
        url = f"https://mempool.space/testnet/api/address/{address}/txs"
    
    try:
        response = requests.get(url)
        nonjson = response.text
        
        if any(error_keyword in nonjson.lower() for error_keyword in ['rpc error', 'too many requests', 'bad request']):
            if network == 'main':
                url = f"https://blockstream.info/api/address/{address}/txs"
                response = requests.get(url)
                nonjson = response.text
    except Exception as e:
        if network == 'main':
            url = f"https://blockstream.info/api/address/{address}/txs"
            response = requests.get(url)
            nonjson = response.text

    json_data = json.loads(nonjson)
    
    txid = None
    vout = None
    amt = None
    
    for tx in json_data:
        for index, output in enumerate(tx["vout"]):
            if output.get("scriptpubkey_address") == address:
                txid = tx.get("txid")
                vout = index
                amt = output.get("value")
                break
    
    return [txid, vout, amt]