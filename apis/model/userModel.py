from sqlalchemy import Column, TEXT, INT, BIGINT
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()

class User(Base):
    __tablename__ = 'member'
    m_id = Column(INT, primary_key=True, autoincrement=True)
    m_relate_type = Column(TEXT, nullable=False)
    m_upper_id = Column(TEXT, nullable=False)
    m_sns_key = Column(TEXT, nullable=False)
    m_sns_type = Column(TEXT, nullable=False)

class userSelectParam(BaseModel):
    m_id: int
    m_relate_type: str
    m_upper_id: str
    m_sns_key : str


class userPutParam(BaseModel):
    m_id: int
    m_relate_type: str
    m_upper_id: str
    m_sns_key : str
    m_sns_type : str

    //ㅇㅎㅎ