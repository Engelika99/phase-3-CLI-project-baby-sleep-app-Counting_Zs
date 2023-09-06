# Baby Sleep App Counting Zs

Baby Sleep App Counting Zs is a simple command-line application that solves a real-world problem for managing baby sleep schedules and parents' information. This application is built using Python, SQLite, SQLAlchemy, and Click. It allows parents to create profiles, add babies, and manage sleep schedules for their babies. Many babies can be added to one parent/caretaker and many schedules can be added to one baby's profile enabling the app to be used in a professional setting such as a school or daycare. 

## Setting up the project:
Set up and run the Baby Sleep App on your local machine. Check that you have Python 3 and SQLite installed.

1. Clone the repository to your local machine:
- git clone

2. Create and Use virrtual environment:
-pipenv install
-pipenv shell

3. Install packages:
* sqlalchemy = "==1.4.41"
* alembic = "*"
* ipdb = "*"
* faker = "*"
* click = "*"
* pytz = "*"

4. Create the SQLite database and tables:
- python seed.py

## What the app can do
   After each command, follow the prompts to input the required information.

   - Create a new parent profile:
  
   `python cli.py create-parent`

   - Add babies to a parent profile:

   `python cli.py create-babies`

   -Create sleep schedules for babies:

   `python cli.py create-sleep-schedule`

   - List sleep schedules for a specific baby:

   `python cli.py list-sleep-schedules`
   
   - Update an existing sleep schedule

   `python cli.py update-sleep-schedule`

   - Delete an existing sleep schedule:

   `python cli.py delete-sleep-schedule`

   - List babies for a specific parent:

   `list-babies`

   ## Database Schema
The Baby Sleep App uses a SQLite database with the following schema:

`parents` table: Stores information about parents name, email, password.
`babies` table: Stores information about babies name, birthday, and their parent relationships.(one-to-many between parents and babies)
`sleep_schedule` table: Stores sleep schedule data for babies.(one-to-many between babies and sleep schedules)

## Contributing
Contributions to the Baby Sleep App are welcome! If you want to contribute fork the repository, create a new branch, make your changes, and submit a pull request.

### License
This project is licensed under the MIT License




