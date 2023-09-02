import click  
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Parent, Baby, BabySleepSchedule, BabySleepRecommendations
from datetime import datetime

# Create database interaction
CountingZs_db = "sqlite:///baby_sleep_app_Counting_Zs.db"
engine = create_engine(CountingZs_db)
Session = sessionmaker(bind=engine)
session = Session()

faker = Faker()
