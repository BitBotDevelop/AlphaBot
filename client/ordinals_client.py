import client.http_client


def query_bitmap_stats():
    """
        查询bitmap的统计信息
    """
    url = "https://turbo.ordinalswallet.com/collection/bitmap/stats"
    print("query bitmap floor price, url:{}".format(url))

    try:
        response = client.http_client.get(url)
        print("response:", response)
        return response
    except Exception as e:
        print("call query bitmap floor price api error", e)
        return None


def query_bitmap_floor_price():
    """
        查询bitmap的地板价信息
    """
    response = query_bitmap_stats()
    if response is not None:
        return response['floor_price']
    else:
        return -1


def inscribe_estimate(receive_address: None, fee_rate: int, filename: str):
    """
        进行铭文交易的链上费用评估
    """
    '''
        查询bitmap的统计信息
    '''
    url = "https://turbo.ordinalswallet.com/inscribe/estimate"
    print("call ordinals wallet api to estimate tx,receive_address:{},fee_rate:{},filename:{}".format(receive_address,
                                                                                                      fee_rate,
                                                                                                      filename))
    # the receive address is only used for estimating the order, so any address is ok 
    if receive_address is None:
        receive_address = "bc1p63zzzdtedgjgf0n2yaelxjzfnsnl32k9cq9ve4ggt9etvvw9l63sgry5qf"
    try:
        headers = {"Content-Type": "application/json"}
        data = {
            "destination": receive_address,
            "fee_rate": fee_rate,
            "postage": 546,
            "content_type": "text/plain",
            "file_sizes": [len(filename)],
        }
        response = client.http_client.post(url=url, data=data, headers=headers)
        print("response:", response)
        return response['total_cost']
    except Exception as e:
        print("call ordinals wallet api to estimate tx error", e)
        return 0
