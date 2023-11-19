import client.http_client
import base64
import json

UNISAT_DOMAIN = "https://open-api.unisat.io"


def create_order(api_key: str, filename: str, receive_address: str, fee_rate: int, dev_address=None):
    """
        创建订单
        return (order_id, amount, pay_address)
    """
    headers = {"Content-Type": "application/json",
               "Authorization": "Bearer " + api_key}

    path = "/v2/inscribe/order/create"
    data = {
        "receiveAddress": receive_address,
        "feeRate": fee_rate,
        "outputValue": 546,
        "files": [
            {
                "filename": filename,
                "dataURL": "data:text/plain;charset=utf-8;base64," + base64.b64encode(filename.encode('utf-8')).decode(
                    'utf-8')
            }
        ],
        "devAddress": dev_address,
        "devFee": 0
    }
    try:
        print("create order,data:{}".format(json.dumps(data)))
        response = client.http_client.post(url=UNISAT_DOMAIN + path, data=data, headers=headers)
        print("response:", response)
        code = response['code']
        if code == 0:
            order_id = response['data']['orderId']
            amount = response['data']['amount']
            pay_address = response['data']['payAddress']
            status = response['data']['status']
            return order_id, amount, pay_address, status
    except Exception as e:
        print('call unisat api to create order failed', e)
        return -1, 0, "", "NONE"


def query_order_detail(api_key: str, order_id: int):
    """
        查询订单详情
    """
    headers = {"Content-Type": "application/json",
               "Authorization": "Bearer " + api_key}

    path = "/v2/inscribe/order/" + str(order_id)

    try:
        print("query order,path:{}".format(UNISAT_DOMAIN + path))
        response = client.http_client.get(url=UNISAT_DOMAIN + path, headers=headers)
        print("response:{}".format(response))
        code = response['code']
        if code == 0:
            return response
    except Exception as e:
        print('call unisat api to query order failed', e)
        return None


def query_order_status(api_key: str, order_id: int):
    """
        查询订单状态, 返回状态为大写
    """
    detail = query_order_detail(api_key, order_id)
    if detail is not None:
        return detail['data']['status'].upper()
    else:
        return "NONE"
