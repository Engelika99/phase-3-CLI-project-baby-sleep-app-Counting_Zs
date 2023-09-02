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
@click.otion('--email', prompt='Enter Your Email', help='Please Enter Your Email')
@click.option('--password', prompt='Enter Your Password', hide_password=True, successful_entry_prompt=True help='Please Enter Your Password')

def create_parent(name, email, password_hash): 
    parents = Parent(name=name, email=email, password_hash=password_hash)
    session.add(parents)
    session.commit()
    click.echo(f"Parent '{name}' Added Successfully!")

