from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Parent(Base):
    __tablename__ = 'parents'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password_hash = Column(String)

    class Baby(Base):
        __tablename__ = 'babies'

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('parent_id'))
    name = Column(String)
    birthday = Column(Date)
    
    password_hash = Column(String)

class BabySleepSchedule(Base):
        __tablename__ = 'sleep schedule'
        id = Column(Integer, primary_key=True)
        baby_id =Column(Integer, ForeignKey('baby_id'))
        sleep_start = Column(DateTime)
        sleep_end = Column(DateTime)

