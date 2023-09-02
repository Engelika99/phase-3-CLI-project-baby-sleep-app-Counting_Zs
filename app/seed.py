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

# create 20 parents
for _ in range(20):
    parents = Parent(
        name=faker.name(),
        email=faker.email(),
        password_hash= faker.password(),
    )
    session.add(parents)


session.commit()    

#parent can have up to 15 babies saved(Teacher/daycare purpose)
parents = session.query(Parent).all()
for parents in parents:
    for _ in range(1, 16):
