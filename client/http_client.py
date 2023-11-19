import requests
import json


def get(url: str, headers=None):
    """
        发起http get请求
    """
    try:
        print("http get,url:{},header:{}".format(url, headers))
        response = requests.get(url=url, headers=headers)
        if response.status_code != 200:
            print("ERROR call http get method failed, status_code:{},message:{}"
                  .format(response.status_code, response.reason))
            return None
        print("response:", response.text)
        return response.json()
    except Exception as e:
        print("ERROR call http get method exception, message:", e)
        return None


def post(url, data, headers=None):
    """
        发起http post请求
    """
    try:
        print("http post,url:{},header:{},data:{}".format(url, json.dumps(headers), json.dumps(data)))
        response = requests.post(url=url, json=data, headers=headers)
        if response.status_code != 200:
            print("ERROR call http post method failed, status_code:{},message:{}"
                  .format(response.status_code, response.reason))
            return None
        return response.json()
    except Exception as e:
        print("ERROR call http post method exception, message:", e)
        return None
