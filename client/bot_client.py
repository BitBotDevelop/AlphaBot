from client.http_client import post
from common.inscribe import generate_brc20_mint_inscribe_content

def inscribe_by_bot(priv: str, tick: str, amt: int, receive_address: str, txid: str, vout: int, amount: int):
    """
        使用bot进行铭文, 因为python生成的代码有一定失败概率无法解决，所以还是先用nodejs实现了一个服务
        代码: https://github.com/BohengLiu/brc20-inscribe-bot/blob/main/src/app/api/brc20/inscribe/route.ts
    """
    url = "https://brc20-inscribe-bot.vercel.app/api/brc20/inscribe"
    body = {
        "secret": priv,
        "text": generate_brc20_mint_inscribe_content(tick, amt),
        "receiveAddress": receive_address,
        "txid": txid,
        "vout": vout,
        "amount": amount
    }
    result = post(url, body)
    print(result)
    return result