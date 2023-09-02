from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Parent, Baby, BabySleepSchedule
from datetime import datetime
from faker import Faker

faker = Faker()

CountingZs_db = "sqlite:///baby_sleep_app_Counting_Zs.db"
engine = create_engine(CountingZs_db)
Session = sessionmaker(bind=engine)
session = Session()

