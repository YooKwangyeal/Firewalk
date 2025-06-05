from sqlalchemy import Column, TEXT, INT
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()

class User(Base):
    __tablename__ = 'member'
    m_id = Column(INT, primary_key=True, autoincrement=True)
    nickname = Column(TEXT)
    email = Column(TEXT)
    m_gender = Column(TEXT)
    m_upper_id = Column(TEXT)
    m_sns_key = Column(TEXT)
    m_sns_type = Column(TEXT)


class userSelectParam(BaseModel):
    m_id: int
    nickname: str = None
    email: str = None
    m_gender: str = None
    m_sns_key: str = None
    m_sns_type: str = None

class userPutParam(BaseModel):
    nickname: str = None
    email: str = None
    m_gender: str = None
    m_sns_key: str = None
    m_sns_type: str = None