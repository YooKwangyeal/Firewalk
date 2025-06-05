from sqlalchemy import Column, TEXT, INT
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()

class User(Base):
    __tablename__ = 'member'
    m_id = Column(INT, primary_key=True, autoincrement=True)
    m_relate_type = Column(TEXT)
    m_upper_id = Column(TEXT)
    m_sns_key = Column(TEXT)
    nickname = Column(TEXT)
    email = Column(TEXT)

class userSelectParam(BaseModel):
    m_id: int
    m_sns_key: str = None
    m_relate_type: str = None
    nickname: str = None
    email: str = None

class userPutParam(BaseModel):
    m_sns_key: str
    m_relate_type: str
    nickname: str = None
    email: str = None