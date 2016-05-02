from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import mapper
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
import settings

DeclarativeBase = declarative_base()

def db_connect():
    return create_engine(URL(**settings.DATABASE), client_encoding='utf-8')

def create_deals_table(engine):
    DeclarativeBase.metadata.create_all(engine)

class Deals(DeclarativeBase):

    __tablename__ = "fsData"

    timestamp = Column('timestamp', String, primary_key=True)
    category = Column('category', String, nullable=True)
    type = Column('type', String, nullable=True)
    address = Column('address', String, nullable=True)
    assignUnit = Column('assignUnit', String, nullable=True)
    status = Column('status', String, nullable=True)
    allData = Column('allData', JSON, nullable=True)