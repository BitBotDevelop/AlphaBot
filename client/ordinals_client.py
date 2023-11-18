import requests

def query_bitmap_stats():
    '''
        查询bitmap的统计信息
    '''
    url = "https://turbo.ordinalswallet.com/collection/bitmap/stats"
    print("query bitmap floor price, url:{}".format(url))
    
    try:
        response = requests.get(url)
        print("response:", response)
        return response
    except Exception as e:
        print("call query bitmap floor price api error", e)
        return None

def query_bitmap_floor_price():
    '''
        查询bitmap的地板价信息
    '''
    response = query_bitmap_stats()
    if response is not None:
        return response['floor_price']
    else:
        return -1
