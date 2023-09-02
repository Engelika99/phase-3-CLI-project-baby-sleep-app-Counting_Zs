import click  
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Parent, Baby, BabySleepSchedule
from datetime import datetime, timedelta

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
        # empty babies list inialized
        babies = []
        baby_count = int(input("Enter the number of babies to add: ")) 
        for _ in range(baby_count):
            baby = Baby(parents=parents, name=faker.first_name(), birthday=faker.date_of_birth())
            babies.append(baby)
            session.add(baby)
        session.commit()
        click.echo(f"{len(babies)} babies added to parent '{parents.name}'!") 

# Create an empty list to store sleep schedules
BabySleepSchedule = []

@click.command()
@click.option('--babies_id', prompt='Baby ID', type=int, help='Baby ID')
@click.option('--sleep_start', prompt='Sleep Start', help='Sleep Start (YYYY-MM-DD HH:MM)')
@click.option('--sleep_end', prompt='Sleep End', help='Sleep End (YYYY-MM-DD HH:MM)')
def create_sleep_schedule(babies_id, sleep_start, sleep_end):
    """Create a new sleep schedule for a baby."""
    
    try:
        sleep_start = datetime.strptime(sleep_start, '%Y-%m-%d %H:%M')
        sleep_end = datetime.strptime(sleep_end, '%Y-%m-%d %H:%M')
    except ValueError:
        click.echo("Invalid date/time format. Please use YYYY-MM-DD HH:MM.")
        return

    new_schedule = BabySleepSchedule(babies_id=babies_id, sleep_start=sleep_start, sleep_end=sleep_end)
    session.add(new_schedule)
    session.commit()

    click.echo(f"Sleep schedule for Baby {babies_id} created.")

    #dictionary to represent the sleep schedule
    schedule = {
        'babies_id': babies_id,
        'sleep_start': sleep_start,
        'sleep_end': sleep_end
    }
    # Append the schedule to the list
    BabySleepSchedule.append(schedule)
    click.echo(f"Sleep schedule for Baby {babies_id} created.")

@click.command()
@click.option('--babies_id', prompt='Baby ID', type=int, help='Baby ID')
def list_sleep_schedules(babies_id):
    """List sleep schedules for a specific baby."""
    schedules = [schedule for schedule in BabySleepSchedule if schedule['babies_id'] == babies_id]
    if not schedules:
        click.echo("No sleep schedules found for this baby.")
    else:
        for schedule in schedules:
            click.echo(f"Baby {babies_id} sleep schedule:")
            click.echo(f"Sleep Start: {schedule['sleep_start']}")
            click.echo(f"Sleep End: {schedule['sleep_end']}")

@click.command()
@click.option('--babies_id', prompt='Baby ID', type=int, help='Baby ID')
@click.option('--schedule_id', prompt='Schedule ID', type=int, help='Schedule ID')
@click.option('--sleep_start', prompt='New Sleep Start', help='New Sleep Start (YYYY-MM-DD HH:MM)')
@click.option('--sleep_end', prompt='New Sleep End', help='New Sleep End (YYYY-MM-DD HH:MM)')
def update_sleep_schedule(babies_id, schedule_id, sleep_start, sleep_end):
    """Update an existing sleep schedule."""
    #sleep start and end times into datetime objects
    sleep_start = datetime.strptime(sleep_start, '%Y-%m-%d %H:%M')
    sleep_end = datetime.strptime(sleep_end, '%Y-%m-%d %H:%M')

    schedule = next((schedule for schedule in BabySleepSchedule if schedule['babies_id'] == babies_id and schedule_id == schedule['schedule_id']), None)
    if schedule:
        schedule['sleep_start'] = sleep_start
        schedule['sleep_end'] = sleep_end
        click.echo(f"Sleep schedule for Baby {babies_id} updated.")
    else:
        click.echo("Sleep schedule not found.")

@click.command()
@click.option('--babies_id', prompt='Baby ID', type=int, help='Baby ID')
@click.option('--schedule_id', prompt='Schedule ID', type=int, help='Schedule ID')
def delete_sleep_schedule(babies_id, schedule_id):
    """Delete an existing sleep schedule."""
    schedule = next((schedule for schedule in BabySleepSchedule if schedule['babies_id'] == babies_id and schedule_id == schedule['schedule_id']), None)
    if schedule:
        BabySleepSchedule.remove(schedule)
        click.echo(f"Sleep schedule for Baby {babies_id} deleted.")
    else:
        click.echo("Sleep schedule not found.")

@click.command()
@click.option('--count', prompt='Number of Schedules', type=int)
def generate_fake_sleep_schedules(count):
    """Generate fake sleep schedules."""
    for _ in range(count):
        babies_id = faker.random_int() 
        sleep_start = faker.date_time_between()
        sleep_end = sleep_start + timedelta(hours=faker.random_int())
        
        schedule = {
            'babies_id': babies_id,
            'sleep_start': sleep_start,
            'sleep_end': sleep_end,
        }
        BabySleepSchedule.append(schedule)
    
    click.echo(f"Generated {count} fake sleep schedules.")

if __name__ == '__main__':
    create_sleep_schedule()
    list_sleep_schedules()
    update_sleep_schedule()
    delete_sleep_schedule()
    generate_fake_sleep_schedules()







