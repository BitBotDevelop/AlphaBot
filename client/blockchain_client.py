import requests

def get_latest_block_number():
    '''
        查询最新的区块高度
    '''
    url = "https://blockchain.info/latestblock"
    print("query lastest block number, url:{}".format(url))
    
    try:
        response = requests.get(url)
        print("response:", response)
        return response['height']
    except Exception as e:
        print("call blockchain api to query lastest block number error", e)
        return 0
