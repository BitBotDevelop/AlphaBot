from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, Depends
from pydantic import BaseModel
import uuid
import time
from typing import List

from server.cron import start_scheduler
from sqlalchemy.orm import Session
from server.database import get_db

from common.inscribe import *

from server.database import Brc20MintTask, Brc20TickInfo
from service.brc20data_service import Brc20Data
from client.blockchain_client import get_gas_fee
from sqlalchemy.orm import defer

brc20_data = Brc20Data(config={})
# 创建 FastAPI 应用程序
app = FastAPI()

# 启动定时任务
start_scheduler()

set_network("testnet")


# 创建一个路由，处理 GET 请求
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


class Brc20MintRequest(BaseModel):
    tick: str
    amt: int
    receive_address: str


@app.post("/api/brc20/mint")
async def mint_brc20(body: Brc20MintRequest, db: Session = Depends(get_db)):
    taskId = uuid.uuid4()
    priv = generate_random_private_key()

    content = generate_brc20_mint_inscribe_content(body.tick, body.amt)
    script = get_text_script_pub_key(priv, content)
    inscriptionAddress = get_inscription_address(priv, script)

    task = Brc20MintTask(
        id=taskId,
        tr_priv=priv,
        tick=body.tick,
        amount=body.amt,
        receive_address=body.receive_address,
        status="waiting_pay",
        inscribe_address=inscriptionAddress,
        created_at=int(time.time()),
        updated_at=int(time.time())
    )
    db.add(task)
    db.commit()

    feeRate = get_gas_fee()
    fee = 152.25 * feeRate + 546

    return {"code": 0, "message": "ok",
            "data": {"taskId": taskId, "inscriptionAddress": inscriptionAddress, "fee": fee}}


@app.get("/internal/api/brc20/mint/tasks")
def query_brc20_mint_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Brc20MintTask).all()
    return {"code": 0, "message": "ok", "data": tasks}


class OrderStatusRequest(BaseModel):
    ids: List[str]


@app.post("/api/brc20/mint/tasks/status")
async def query_brc20_mint_orders_by_ids(body: OrderStatusRequest, db: Session = Depends(get_db)):
    ids = body.ids
    print(ids)
    tasks = db.query(Brc20MintTask).filter(Brc20MintTask.id.in_(ids)).options(defer(Brc20MintTask.tr_priv)).all()
    return {"code": 0, "message": "ok", "data": tasks}


class MintRankRequest(BaseModel):
    period: str
    top_n: int

@app.post("/api/brc20/mint/rank")
def query_brc20_mint_rank(body: MintRankRequest):
    """
        根据用户选择的top_n参数来展示结果,top_n表示当前mint_progress倒排后的结果
    """
    data = brc20_data.get_minting_rank(body.top_n, body.period)
    return {"code": 0, "message": "success", "data": data}


@app.get("/api/brc20/tick/info/{tick}")
def query_brc20_tick_info(tick: str):
    """
        查询brc20 tick的详情,用户mint时查询的数据
    """
    data = brc20_data.get_tick_info(tick)
    return {"code": 0, "message": "success", "data": data}


class AddBrc20TickRequest(BaseModel):
    ticks: str
    
    
@app.post("/api/brc20/ticks/add")
def add_brc20_ticks(body: AddBrc20TickRequest, db: Session = Depends(get_db)):
    """
        添加brc20 ticks
    """
    ticks = body.ticks
    print("add_brc20_ticks:{}".format(ticks))
    if ticks is not None and ticks != '':
        tick_list = ticks.split(",")
        for tick in tick_list:
            tick_info = brc20_data.get_tick_info(tick)
            tick_model = db.query(Brc20TickInfo).filter_by(tick=tick).first()
            if tick_model is not None:
                # 更新
                tick_model.minted=tick_info['minted']
                tick_model.mint_progress=tick_info['mint_progress']
                tick_model.transactions=tick_info['transactions']
                tick_model.holders=tick_info['holders']
                tick_model.updated_at=int(time.time())
                
            else:
                # 新增
                tick_model = Brc20TickInfo(
                    inscription_id = tick_info['inscription_id'],
                    tick = tick_info['tick'],
                    
                    inscription_number =tick_info['inscription_number'],
                    max = tick_info['max'],
                    limit = tick_info['limit'],
                    decimals = tick_info['decimals'],
                    minted = tick_info['minted'],
                    mint_progress = tick_info['mint_progress'],
                    transactions = tick_info['transactions'],
                    holders = tick_info['holders'], 
                    deployer = tick_info['deployer'],
                    deploy_time =tick_info['deploy_time'],
                    created_at = int(time.time()),
                    updated_at = int(time.time())
                )
                db.add(tick_model)
            db.commit()
            
    
    return {"code": 0, "message": "insert or update success", "data": []}

class DeleteBrc20TickRequest(BaseModel):
    ticks: str
    
@app.post("/api/brc20/ticks/delete")
def add_brc20_ticks(body: DeleteBrc20TickRequest, db: Session = Depends(get_db)):
    """
        删除brc20 ticks
    """
    ticks = body.ticks
    if ticks is not None and ticks != '':
        num = db.query(Brc20TickInfo).filter(Brc20TickInfo.tick.in_(ticks.split(","))).delete(synchronize_session=False)
        db.commit()
        print("delete ticks:{} succees, num:{}".format(ticks, num))
        
    return {"code": 0, "message": "delete success", "data": [ticks]}
        

@app.get("/api/brc20/ticks/list")
def add_brc20_ticks(db: Session = Depends(get_db)):
    ticks = db.query(Brc20TickInfo).all()
    return {"code": 0, "message": "ok", "data": ticks}
