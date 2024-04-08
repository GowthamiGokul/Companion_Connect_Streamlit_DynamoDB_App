import mysql.connector
import sqlite3
import pandas as pd
from sqlalchemy import create_engine

config = {
  'user': 'root',
  'password': 'root',
  'host': '127.0.0.1',
  'port': 3306,
  'database': 'animal_shelter',
  'raise_on_warnings': True
}

mydb = mysql.connector.connect(**config)
engine = create_engine('sqlite:///animal_shelter.db')


# Laxmikant Contributed and helped

def display():

    # Fetch all Animals who were abandoned before
    my_cursor = mydb.cursor(dictionary=True)
    my_cursor.execute("SELECT * FROM Intakes WHERE IntakeReason='Abandoned'")
    for out in my_cursor:
        print(out)

    # Adoption History and Trial Adoptions to list all animals that are currently on a trial adoption along with their movement date and return date.
    my_cursor.execute("SELECT Animals.AnimalName,Movements.MovementDate,Movements.ReturnDate,Movements.MovementType, \
                      Movements.IsTrial FROM Movements\
                    JOIN Animals ON Movements.AnimalID = Animals.AnimalID WHERE Movements.MovementType = 'Adoption' AND Movements.IsTrial = 1;")
    for out in my_cursor:
        print(out)

    # Deceased Animals Report to track animals that have passed away, focusing on the reason and whether it happened in or out of the shelter.
    my_cursor.execute("SELECT Animals.AnimalName, Deceased.DeceasedDate, Deceased.DeceasedReason, Deceased.DiedOffShelter\
                        FROM Deceased JOIN Animals ON Deceased.AnimalID = Animals.AnimalID WHERE Deceased.DeceasedDate IS NOT NULL\
                        ORDER BY Deceased.DeceasedDate DESC;")
    for out in my_cursor:
        print(out)
    



# Gowthami Contributed and helped
def createDB():
    # Establish a connection to the database (this will create the database file if it doesn't exist)
    conn = sqlite3.connect('animal_shelter.db')
    cursor = conn.cursor()

    # Define the SQL statements for creating the tables
    create_tables_sql = [
        """
        CREATE TABLE Animals (
            AnimalID INTEGER PRIMARY KEY AUTOINCREMENT,
            ShelterCode TEXT NOT NULL UNIQUE,
            IdentichipNumber TEXT UNIQUE,
            AnimalName TEXT NOT NULL,
            SpeciesName TEXT NOT NULL,
            BaseColour TEXT,
            AnimalAge TEXT,
            SexName TEXT,
            CONSTRAINT UC_Animal UNIQUE (ShelterCode, IdentichipNumber)
        );
        """,
        """
        CREATE TABLE Species (
            SpeciesID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT UNIQUE NOT NULL
        );
        """,
        """
        CREATE TABLE Breeds (
            BreedID INTEGER PRIMARY KEY AUTOINCREMENT,
            SpeciesID INTEGER NOT NULL,
            Name TEXT NOT NULL,
            FOREIGN KEY (SpeciesID) REFERENCES Species(SpeciesID)
        );
        """,
        """
        CREATE TABLE Intakes (
            IntakeID INTEGER PRIMARY KEY AUTOINCREMENT,
            AnimalID INTEGER,
            IntakeDate DATE NOT NULL,
            IntakeReason TEXT,
            IsTransfer BOOLEAN,
            FOREIGN KEY (AnimalID) REFERENCES Animals(AnimalID)
        );
        """,
        """
        CREATE TABLE Movements (
            MovementID INTEGER PRIMARY KEY AUTOINCREMENT,
            AnimalID INTEGER,
            MovementDate DATE NOT NULL,
            MovementType TEXT NOT NULL,
            IsTrial BOOLEAN,
            ReturnDate DATE,
            ReturnedReason TEXT,
            FOREIGN KEY (AnimalID) REFERENCES Animals(AnimalID)
        );
        """,
        """
        CREATE TABLE Deceased (
            DeceasedID INTEGER PRIMARY KEY AUTOINCREMENT,
            AnimalID INTEGER,
            DeceasedDate DATE,
            DeceasedReason TEXT,
            DiedOffShelter BOOLEAN,
            PutToSleep BOOLEAN,
            IsDOA BOOLEAN,
            FOREIGN KEY (AnimalID) REFERENCES Animals(AnimalID)
        );
        """,
        """
        CREATE TABLE Locations (
            LocationID INTEGER PRIMARY KEY AUTOINCREMENT,
            AnimalID INTEGER,
            Description TEXT NOT NULL,
            FOREIGN KEY (AnimalID) REFERENCES Animals(AnimalID)
        );
        """
    ]

    # Execute each CREATE TABLE statement
    for sql in create_tables_sql:
        cursor.execute(sql)


    conn.commit()
    conn.close()




def insert_csv_to_sql(csv_file_path, table_name, engine, index_label=None):
    df = pd.read_csv(csv_file_path)
    df.to_sql(table_name, con=engine, if_exists='append', index=False, index_label=index_label)



if __name__=="__main__":
    createDB()
    insert_csv_to_sql('animals.csv', 'Animals', engine)
    insert_csv_to_sql('species.csv', 'Species', engine)
    insert_csv_to_sql('breeds.csv', 'Breeds', engine)
    insert_csv_to_sql('intake.csv', 'Intakes', engine)
    insert_csv_to_sql('movements.csv', 'Movements', engine)
    insert_csv_to_sql('deceased.csv', 'Deceased', engine)
    insert_csv_to_sql('location.csv', 'Locations', engine)


