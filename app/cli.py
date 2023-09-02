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

@click.group()
def cli():
    pass

@click.command()
@click.option('--name', prompt='Enter Your Name', help='Please Enter Your User Name')
@click.option('--email', prompt='Enter Your Email', help='Please Enter Your Email')
@click.option('--password_hash', prompt='Enter Your Password', hide_input=True, help='Please Enter Your Password')

def create_parent(name, email, password_hash): 
    if not name:
        name = faker.name()
    if not email:
        email = faker.email()
    if not password_hash:
        password_hash = faker.password()
    parents = Parent(name=name, email=email, password_hash=password_hash)
    session.add(parents)
    session.commit()
    click.echo(f"Parent '{name}' Added Successfully!")

@click.command()
@click.option('--parents_id', prompt='Parent ID', type=int, help='Parent ID')

def create_babies(parents_id):
    parents = session.query(Parent).get(parents_id)
    if parents: 
        babies = []
        baby_count = int(input("Enter the number of babies to add: ")) 
        for _ in range(baby_count):
            baby = Baby(parents=parents, name=faker.first_name(), birthday=faker.date_of_birth())
            babies.append(baby)
            session.add(baby)
        session.commit()
        click.echo(f"{len(babies)} babies added to parent '{parents.name}'!") 






