"""
提供brc20的数据接口
"""
import client.http_client

default_api_key = "142cf1b0-1ca7-11ee-bb5e-9d74c2e854ac"

def get_brc20_list():
    """
        获取所有brc20列表
        :return [
            {"tick": "ordi",
            "inscription_id": "b61b0172d95e266c18aea0c624db987e971a5d6d4ebc2aaed85da4642d635735i0",
            "inscription_number": 348020, "max": "21000000.000000000000000000",
            "limit": "1000.000000000000000000",
            "decimals": 18,
            "minted": "21000000.000000000000000000",
            "mint_progress": "1.000000",
            "transactions": 207945,
            "holders": 12707,
            "deployer": "bc1pxaneaf3w4d27hl2y93fuft2xk6m4u3wc4rafevc6slgd7f5tq2dqyfgy06",
            "deploy_time": 1678248991
            }
        ]
    """
    page_size = 1000
    offset = 0
    limit = page_size + offset
    total = limit
    brc20_list = []
    while limit <= total:
        if offset >= limit:
            break
        url = "https://api.geniidata.com/api/1/brc20/ticks?limit={}&offset={}".format(limit, offset)
        print(url)
        headers = {
            "accept": "application/json",
            "api-key": "142cf1b0-1ca7-11ee-bb5e-9d74c2e854ac"
        }

        response = client.http_client.get(url, headers=headers)
        if response['code'] == 0:
            count = response['data']['count']
            brc20_list.extend(response['data']['list'])
            if total <= count:
                total = count
            limit = min(total, limit + page_size)
            offset += page_size
        else:
            print("error, get brc20 ticks error, response:", response)
    return brc20_list


def get_brc20_mint_rank(api_key: str, period="1D"):
    """
        根据指定的周期来查询mint中的brc20_list
        :return:
        {
            "rows":[{
                "inscriptionNumber": 396419,
                "inscriptionId": "42dd980ad18bc5b57bb6900377b65e27cb2d7a9d5c1b993347d84c62db0dd80ei0",
                "mints": "254654",
                "tick": "mice"
            }],
            "minted":{
                "c7ee58a761f23d68b4a35c16f25e96fe9317a63d8a951eff9773099ba08cb6adi0": {
                "max": "1000000000000",
                "minted": "367775621",
                "holders": 5470,
                "mintConfirmedBefore24h": "367515210",
                "mintConfirmedBetween1h24h": "260411",
                "mintConfirmedIn1h": "0",
                "mintMemPool": "7535800"
            },
            }
        }
    """
    if api_key is None:
        api_key = default_api_key
    url = "https://www.geniidata.com/api/btc/ord/flow/rank?p=brc20&type={}".format(period)
    headers = {
        "accept": "application/json",
        "api-key": api_key
    }
    response = client.http_client.get(url, headers=headers)
    if response['code'] == 0:
        return response['data']
    else:
        return None


def get_brc20_tick_info(api_key: str, tick: str):
    """
        获取brc20的tick信息:
        :return
        {
            "code":0,
            "message":"success",
            "data":{
                "tick":"ordi",
                "inscription_id":"b61b0172d95e266c18aea0c624db987e971a5d6d4ebc2aaed85da4642d635735i0",
                "inscription_number":348020,
                "max":"21000000.000000000000000000",
                "limit":"1000.000000000000000000",
                "decimals":18,
                "minted":"21000000.000000000000000000",
                "mint_progress":"1.000000",
                "transactions":207983,
                "holders":12712,
                "deployer":"bc1pxaneaf3w4d27hl2y93fuft2xk6m4u3wc4rafevc6slgd7f5tq2dqyfgy06",
                "deploy_time":1678248991
            }
        }
    """
    if api_key is None:
        api_key = default_api_key

    if tick == "" or tick is None:
        raise ValueError("Invalid tick")
    url = "https://api.geniidata.com/api/1/brc20/tickinfo/{}".format(tick)
    headers = {
        "accept": "application/json",
        "api-key": api_key
    }

    response = client.http_client.get(url, headers=headers)
    if response['code'] == 0:
        return response['data']
    else:
        return {}


def get_brc20_alpha_signals(api_key: str, op: int = 1):
    """
        查找brc20的alpha数据，跟单
        @param: op:空，所有 1:mint, 2:sell, 3:buy
    """
    if api_key is None:
        api_key = default_api_key

    url = "https://www.geniidata.com/api/btc/ord/flow/activity?op={}&p=brc20".format(op)
    headers = {
        "accept": "application/json",
        "api-key": api_key
    }

    response = client.http_client.get(url, headers=headers)
    if response['code'] == 0:
        return response['data']
    else:
        return []
