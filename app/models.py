from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import timedelta


Base = declarative_base()

class Parent(Base):
    __tablename__ = 'parents'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password_hash = Column(String)
    babies = relationship('Baby', back_populates='parents')

class Baby(Base):
    __tablename__ = 'babies'

    id = Column(Integer, primary_key=True)
    parents_id = Column(Integer, ForeignKey('parents.id'))
    name = Column(String)
    birthday = Column(Date)
    parents = relationship('Parent', back_populates='babies')
    sleep_schedule = relationship('BabySleepSchedule', back_populates='babies')
 

class BabySleepSchedule(Base):
        __tablename__ = 'sleep_schedule'
        id = Column(Integer, primary_key=True)
        babies_id =Column(Integer, ForeignKey('babies.id'))
        sleep_start = Column(DateTime)
        sleep_end = Column(DateTime)
        babies = relationship('Baby', back_populates='sleep_schedule')
        
        

        def __init__(self, babies_id, sleep_start, sleep_end):
             self.babies_id = babies_id
             self.sleep_start = sleep_start
             self.sleep_end = sleep_end
        @property
        def sleep_amount(self):
            duration = self.sleep_end - self.sleep_start
            duration = timedelta(seconds=duration.seconds)
            hours = duration.seconds // 3600
            minutes = (duration.seconds // 60) % 60
            return f"{hours} hours and {minutes} minutes"


     