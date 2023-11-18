import requests
import base64

UNISAT_DOMAIN = "https://open-api.unisat.io"

def create_order(apiKey: str, fileName: str, receiveAddress: str, feeRate: int, devAddress = None):
    '''
        创建订单
    '''
    headers = {"Content-Type":"application/json",
              "Authorization":"Bearer " + apiKey}
    
    path = "/v2/inscribe/order/create"
    data = {
        "receiveAddress": receiveAddress,
        "feeRate":feeRate,
        "outputValue":546,
        "files":[
            {
                "filename":fileName,
                "dataURL":"data:text/plain;charset=utf-8;base64," + base64.b64encode(fileName.encode('utf-8')).decode('utf-8')
            }
        ],
        "devAddress":devAddress,
        "devFee":0
    }
    try:
        print("create order,data:{}".format(data))
        response = requests.post(url=UNISAT_DOMAIN + path, data=data, headers=headers)
        print("response:{}".format(response))
        code = response['code']
        if code == 0:
            return response['order'], response['data']['amount']
    except Exception as e:
        print('call unisat api to create order failed', e)
        return -1, 0
    
def query_order_detail(apiKey: str, orderId: int):
    '''
        查询订单详情
    '''
    headers = {"Content-Type":"application/json",
              "Authorization":"Bearer " + apiKey}
    
    path = "/v2/inscribe/order/" + str(orderId)
    
    try:
        print("query order,path:{}".format(UNISAT_DOMAIN + path))
        response = requests.get(url=UNISAT_DOMAIN + path, headers=headers)
        print("response:{}".format(response))
        code = response['code']
        if code == 0:
            return response
    except Exception as e:
        print('call unisat api to query order failed', e)
        return None
    
def query_order_status(apiKey: str, orderId: int):
    '''
        查询订单状态, 返回状态为大写
    '''
    detail = query_order_detail(apiKey, orderId)
    if detail is not None:
        return detail['data']['status'].upper()
    else:
        return "NONE"
    
    