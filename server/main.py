from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
import uuid
import time
from typing import List

from server.cron import start_scheduler
from sqlalchemy.orm import Session
from server.database import get_db, User

from common.inscribe import *

from server.database import Brc20MintTask
from client.blockchain_client import get_gas_fee
from sqlalchemy.orm import defer

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
    
    return {"code": 0, "message": "ok", "data": {"taskId": taskId, "inscriptionAddress": inscriptionAddress, "fee": fee }}

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