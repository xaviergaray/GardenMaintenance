import os
import sqlite3 as sql


class Garden:
    COLUMNS = ['name', 'water_freq', 'fertilizer_freq', 'temp_min', 'temp_max', 'humidity_min', 'humidity_max']

    def __init__(self, connection):
        self.db_connection = connection

    def create_table(self):
        cursor = self.db_connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS plants (PK INTEGER PRIMARY KEY, name TEXT, water_freq TEXT, fertilizer_freq TEXT, temp_min INTEGER, temp_max INTEGER, humidity_min INTEGER, humidity_max INTEGER)")
        self.db_connection.commit()

    def insert_plant(self, name, water_freq, fertilizer_freq, temp_min, temp_max, humidity_min, humidity_max):
        cursor = self.db_connection.cursor()
        cursor.execute(
            "INSERT INTO plants (name, water_freq, fertilizer_freq, temp_min, temp_max, humidity_min, humidity_max) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (name, water_freq, fertilizer_freq, temp_min, temp_max, humidity_min, humidity_max)
        )
        self.db_connection.commit()

    def delete_plant(self, PK):
        cursor = self.db_connection.cursor()
        cursor.execute("DELETE FROM plants WHERE PK=?", (PK,))
        self.db_connection.commit()

    def update_plant(self, PK, column, value):
        if column not in self.COLUMNS:
            raise ValueError(f"Invalid column name: {column}")
        cursor = self.db_connection.cursor()
        cursor.execute(f"UPDATE plants SET {column} = ? WHERE PK = ?", (value, PK))
        self.db_connection.commit()

    def select_plant(self, PK):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM plants WHERE PK=?", (PK,))
        return cursor.fetchone()


if __name__ == "__main__":
    directory = '../out'
    bFirstPass = False

    if not os.path.isdir(directory):
        bFirstPass = True
        os.makedirs(directory, exist_ok=True)

    conn = sql.connect('../out/plants.db')

    garden = Garden(conn)
    if bFirstPass:
        garden.create_table()

    while True:
        print("1. Insert a plant")
        print("2. Delete a plant")
        print("3. Update a plant")
        print("4. Select a plant")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter plant name (press enter for null): ") or None
            water_freq = input("Enter water frequency (press enter for null): ") or None
            fertilizer_freq = input("Enter fertilizer frequency (press enter for null): ") or None
            temp_min = input("Enter minimum temperature (press enter for null): ")
            temp_min = int(temp_min) if temp_min else None
            temp_max = input("Enter maximum temperature (press enter for null): ")
            temp_max = int(temp_max) if temp_max else None
            humidity_min = input("Enter minimum humidity (press enter for null): ")
            humidity_min = int(humidity_min) if humidity_min else None
            humidity_max = input("Enter maximum humidity (press enter for null): ")
            humidity_max = int(humidity_max) if humidity_max else None
            garden.insert_plant(name, water_freq, fertilizer_freq, temp_min, temp_max, humidity_min, humidity_max)
        elif choice == '2':
            PK = int(input("Enter plant PK to delete: "))
            garden.delete_plant(PK)
        elif choice == '3':
            PK = int(input("Enter plant PK to update: "))
            column = input("Enter column to update: ")
            value = input("Enter new value (press enter for null): ") or None
            garden.update_plant(PK, column, value)
        elif choice == '4':
            PK = int(input("Enter plant PK to select: "))
            print(garden.select_plant(PK))
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")


