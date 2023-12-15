from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Boolean
import os

DATABASE_URL = os.environ.get("DATABASE_URL")  
engine = create_engine(DATABASE_URL)

Base = declarative_base()


class Brc20MintTask(Base):
    __tablename__ = "brc20_mint_tasks"

    id = Column(String(128), primary_key=True, index=True)
    tr_priv = Column(String(128), unique=False, index=False)
    tick = Column(String(32), unique=False, index=False)
    amount = Column(Integer, unique=False, index=False)
    receive_address = Column(String(128), unique=False, index=False)
    inscribe_address = Column(String(128), unique=False, index=False)
    created_at = Column(Integer, unique=False, index=True)
    updated_at = Column(Integer, unique=False, index=True)
    status = Column(String(32), unique=False, index=True) # waiting_pay, waiting_mint, minted, failed, waiting_refund, refunded

class Brc20TickInfo(Base):
    __tablename__ = "brc20_tick_info"
    
    inscription_id = Column(String(128), primary_key=True, index=True)
    tick = Column(String(32), unique=False, index=True)
    
    inscription_number = Column(Integer, unique=False, index=False)
    max = Column(String(64), unique=False, index=False)
    limit = Column(String(32), unique=False, index=False)
    decimals = Column(Integer, unique=False, index=False)
    minted = Column(String(64), unique=False, index=False)
    mint_progress = Column(String(32), unique=False, index=False)
    transactions = Column(Integer, unique=False, index=False) 
    holders = Column(Integer, unique=False, index=False) # 
    deployer = Column(String(128), unique=False, index=False) #
    deploy_time = Column(Integer, unique=False, index=False) # 
    created_at = Column(Integer, unique=False, index=False)
    updated_at = Column(Integer, unique=False, index=False)

# 创建数据库表
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
