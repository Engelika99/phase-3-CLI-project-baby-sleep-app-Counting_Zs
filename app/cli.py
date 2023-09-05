import click
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Parent, Baby, BabySleepSchedule
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
    click.echo(f"Parent '{name}' (ID: {parents.id} Added Successfully!")

cli.add_command(create_parent)

@click.command()
@click.option('--parents_id', prompt='Parent ID', type=int, help='Parent ID')
def create_babies(parents_id):
    parents = session.query(Parent).get(parents_id)
    if parents:
        # empty babies list initialized
        babies = []
        baby_count = int(input("Enter the number of babies to add: "))
        for _ in range(baby_count):
            baby = Baby(parents=parents, name=faker.first_name(), birthday=faker.date_of_birth())
            babies.append(baby)
            session.add(baby)
        session.commit()
        click.echo(f"{len(babies)} babies added to parent '{parents.name} (ID: {parents.id})'!")

cli.add_command(create_babies)

# Create an empty list to store sleep schedules
baby_sleep_schedule = []

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

    # Dictionary to represent the sleep schedule
    schedule = {
        'babies_id': babies_id,
        'sleep_start': sleep_start,
        'sleep_end': sleep_end
    }
    # Append the schedule to the list
    baby_sleep_schedule.append(schedule)
    click.echo(f"Sleep schedule for Baby {babies_id} created.")

cli.add_command(create_sleep_schedule)

@click.command()
@click.option('--babies_id', prompt='Baby ID', type=int, help='Baby ID')
def list_sleep_schedules(babies_id):
    """List sleep schedules for a specific baby."""
    schedules = session.query(BabySleepSchedule).filter_by(babies_id=babies_id).all()
    if not schedules:
        click.echo("No sleep schedules found for this baby.")
    else:
        for schedule in schedules:
            click.echo(f"Baby {babies_id} sleep schedule:")
            click.echo(f"Schedule ID: {schedule.id}")
            click.echo(f"Sleep Start: {schedule.sleep_start}")
            click.echo(f"Sleep End: {schedule.sleep_end}")

cli.add_command(list_sleep_schedules)

@click.command()
@click.option('--babies_id', prompt='Baby ID', type=int, help='Baby ID')
@click.option('--schedule_id', prompt='Schedule ID', type=int, help='Schedule ID')
@click.option('--sleep_start', prompt='New Sleep Start', help='New Sleep Start (YYYY-MM-DD HH:MM)')
@click.option('--sleep_end', prompt='New Sleep End', help='New Sleep End (YYYY-MM-DD HH:MM)')
def update_sleep_schedule(babies_id, schedule_id, sleep_start, sleep_end):
    """Update an existing sleep schedule."""
    # Sleep start and end times into datetime objects
    sleep_start = datetime.strptime(sleep_start, '%Y-%m-%d %H:%M')
    sleep_end = datetime.strptime(sleep_end, '%Y-%m-%d %H:%M')

    # Check if the sleep schedule exists in the database
    schedule = session.query(BabySleepSchedule).filter_by(babies_id=babies_id, id=schedule_id).first()
    if schedule:
        schedule.sleep_start = sleep_start
        schedule.sleep_end = sleep_end
        session.commit()
        click.echo(f"Sleep schedule for Baby {babies_id} updated.")
    else:
        click.echo("Sleep schedule not found.")

cli.add_command(update_sleep_schedule)

@click.command()
@click.option('--babies_id', prompt='Baby ID', type=int, help='Baby ID')
@click.option('--schedule_id', prompt='Schedule ID', type=int, help='Schedule ID')
def delete_sleep_schedule(babies_id, schedule_id):
    """Delete an existing sleep schedule."""
    # Check if the sleep schedule exists in the database
    schedule = session.query(BabySleepSchedule).filter_by(babies_id=babies_id, id=schedule_id).first()
    if schedule:
        session.delete(schedule)
        session.commit()
        click.echo(f"Sleep schedule for Baby {babies_id} deleted.")
    else:
        click.echo("Sleep schedule not found.")

cli.add_command(delete_sleep_schedule)

@click.command()
@click.option('--parents_id', prompt='Parent ID', type=int, help='Parent ID')
def list_babies(parents_id):
    """List babies for a specific parent."""
    parent = session.query(Parent).get(parents_id)
    if parent:
        babies = parent.babies
        if not babies:
            click.echo(f"No babies found for Parent {parent.name}.")
        else:
            click.echo(f"Babies for Parent {parent.name}:")
            for baby in babies:
                click.echo(f"Baby ID: {baby.id}")
                click.echo(f"Baby Name: {baby.name}")
                click.echo(f"Baby Birthday: {baby.birthday}")
    else:
        click.echo("Parent not found.")

cli.add_command(list_babies)

if __name__ == "__main__":
    cli()
