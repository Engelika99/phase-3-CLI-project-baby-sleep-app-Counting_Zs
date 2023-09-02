from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Parent, Baby, BabySleepSchedule
from datetime import timedelta
from faker import Faker
import pytz 

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
for parent in parents:
    for _ in range(1, 16):
        babies = Baby(
            parents=parent,
            name=faker.first_name(),
            birthday = faker.date_of_birth(minimum_age=0, maximum_age=3 ) 
        )
        session.add(babies)


session.commit()        

#Create random slepp schedules
babies = session.query(Baby).all()
for baby in babies:
    for _ in range(3):
        sleep_start = faker.date_time_between(start_date='-1y', end_date='now', tzinfo=pytz.utc)
        user_timezone = pytz.timezone('America/New_York')
        sleep_start_local = sleep_start.astimezone(user_timezone)
        sleep_end = sleep_start + timedelta(hours=faker.random_int(min=1, max=12))
        schedule = BabySleepSchedule(
            babies=baby,
            sleep_start=sleep_start,
            sleep_end=sleep_end
        )
        session.add(schedule)


session.commit()



if __name__ == '__main__':
    session.close()