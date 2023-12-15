from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from server.database import get_db, Brc20MintTask, Brc20TickInfo, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy.sql import asc
from common.inscribe import *
from client.blockchain_client import address_once_had_money, address_received_money_in_this_tx, broadcast_tx
from client.bot_client import inscribe_by_bot
import time
from datetime import datetime

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
    new_status = "waiting_pay"
    if result:
        new_status = "waiting_mint"
        [txid, vout, amount] = await address_received_money_in_this_tx(address, network="testnet")
        result = inscribe_by_bot(priv, tick, amt, receive_address, txid, vout, amount)
        print(result['code'], result['data']['result'])
        if result['code'] == 0 and ('-27' in result['data']['result'] or "sendrawtransaction RPC error" not in result['data']['result']):
            new_status = "minted"

    return new_status


is_running = False
# 定义一个定时任务函数
async def scheduled_task():
    """
    定时拉取订单，并处理
    """
    global db
    print("定时任务执行")
    global is_running  # 将 is_running 声明为全局变量
    if is_running:
        return
    is_running = True
    try:
        # 获得时间
        now = int(time.time())
        tasks = db.query(Brc20MintTask).filter(Brc20MintTask.status == "waiting_pay").filter(Brc20MintTask.created_at > now - 600).order_by(asc(Brc20MintTask.updated_at)).all()
        for task in tasks:
            print(task.id, task.tr_priv, task.tick, task.amount, task.receive_address)
            new_status = await handle_task(task.tr_priv, task.tick, task.amount, task.receive_address)
            if new_status != task.status:
                db.query(Brc20MintTask).filter(Brc20MintTask.id == task.id).update({
                    "status": new_status,
                    "updated_at": int(time.time())
                })
                db.commit()
    finally:
        is_running = False
    

# 添加一个定时任务，每隔5秒执行一次
scheduler.add_job(scheduled_task, "interval", seconds=10)


# 调度任务定时更新brc20 ticks
back_scheduler = BackgroundScheduler()
from service.brc20data_service import Brc20Data
brc20_data = Brc20Data(config={})


def update_brc20_ticks_info():
    print("crane scheduler update_brc20_ticks_info,time:{}".format(datetime.now().strftime("%Y%m%d %H:%M:%S")))
    ticks = db.query(Brc20TickInfo).all()
    # 如果tick的mint_process不为1,则更新
    for tick in ticks:
        if float(tick.mint_progress) == 1:
            print('tick:{} has been minted over'.format(tick.tick))
            continue
        tick_info = brc20_data.get_tick_info(tick.tick)
        tick_model = db.query(Brc20TickInfo).filter_by(tick=tick.tick).first()
        if tick_model is not None:
            # 更新
            tick_model.minted = tick_info['minted']
            tick_model.mint_progress = tick_info['mint_progress']
            tick_model.transactions = tick_info['transactions']
            tick_model.holders = tick_info['holders']
            tick_model.updated_at = int(time.time())
        db.commit()

# 每5分钟调度一次
back_scheduler.add_job(update_brc20_ticks_info, trigger="interval", minutes=5)


def start_scheduler():
    # 启动定时任务调度器
    if not scheduler.running:
        print("scheduler start")
        scheduler.start()
    else:
        print("scheduler is running")

    # 启动定时任务调度器
    if not back_scheduler.running:
        print("back_scheduler start")
        back_scheduler.start()
    else:
        print("back_scheduler is running")
