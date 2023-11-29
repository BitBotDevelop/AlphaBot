from apscheduler.schedulers.asyncio import AsyncIOScheduler
from server.database import get_db, Brc20MintTask, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy.sql import asc
from common.inscribe import *
from client.blockchain_client import address_once_had_money, address_received_money_in_this_tx, broadcast_tx

is_running = False

db = SessionLocal()
# 创建一个定时任务调度器
scheduler = AsyncIOScheduler()

async def handle_task(priv: str, tick: str, amt: int, receive_address: str):
    """
        处理一个任务
    """
    # 生成铭文地址
    print("处理任务", priv, tick, amt, receive_address)
    inscribe_content = generate_brc20_mint_inscribe_content(tick, amt)
    tr_script = get_text_script_pub_key(priv, inscribe_content)
    address = get_inscription_address(priv, tr_script)
    print("铭文地址", address)
    result = await address_once_had_money(address, network="testnet")
    if result:
      [txid, vout, amount] = await address_received_money_in_this_tx("tb1p52ex09p6en3czr0rs7sn5q2zw5t6ueasxtvnfshfe2ef2h2x5khqh2h5qm", network="testnet")
      [txhex, vsize, newTxid ] = inscribe_from_tr_script(txid, vout, amount, priv, tr_script, receive_address)
      print(txhex)
      resp = broadcast_tx(txhex)
      print(resp.text)
      

is_running = False
# 定义一个定时任务函数
async def scheduled_task():
    global db
    print("定时任务执行")
    global is_running  # 将 is_running 声明为全局变量
    if is_running:
        return
    is_running = True
    try:
      tasks = db.query(Brc20MintTask).filter(Brc20MintTask.status == "waiting_pay").order_by(asc(Brc20MintTask.updated_at)).all()
      for task in tasks:
          print(task.id, task.tr_priv, task.tick, task.amount, task.receive_address)
          await handle_task(task.tr_priv, task.tick, task.amount, task.receive_address)
    finally:
      is_running = False
    

# 添加一个定时任务，每隔5秒执行一次
scheduler.add_job(scheduled_task, "interval", seconds=5)


def start_scheduler():
    # 启动定时任务调度器
    scheduler.start()
