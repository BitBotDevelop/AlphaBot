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

    id = Column(String, primary_key=True, index=True)
    tr_priv = Column(String, unique=False, index=False)
    tick = Column(String, unique=False, index=False)
    amount = Column(Integer, unique=False, index=False)
    receive_address = Column(String, unique=False, index=False)
    inscribe_address = Column(String, unique=False, index=False)
    created_at = Column(Integer, unique=False, index=True)
    updated_at = Column(Integer, unique=False, index=True)
    status = Column(String, unique=False, index=True) # waiting_pay, waiting_mint, minted, failed, waiting_refund, refunded


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
