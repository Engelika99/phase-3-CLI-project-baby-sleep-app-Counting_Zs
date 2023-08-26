from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Parent(Base):
    __tablename__ = 'parents'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password_hash = Column(String)