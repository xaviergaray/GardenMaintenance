import os
import sqlite3 as sql
import threading
from config import DB_FILEPATH


class Garden:
    def __init__(self):
        self.COLUMNS = ['name', 'water_freq', 'fertilizer_freq', 'temp_min', 'temp_max', 'humidity_min', 'humidity_max']

        if not os.path.isdir(DB_FILEPATH):
            os.makedirs(DB_FILEPATH)

        # Thread-local storage for the database connection and cursor
        self.local_storage = threading.local()
        self.create_table()

    def __del__(self):
        self.close_connection()

    def get_connection(self):
        # Check if connection already exists in local storage for this thread
        if not hasattr(self.local_storage, 'connection'):
            self.local_storage.connection = sql.connect(str(DB_FILEPATH) + '/plants.db')
            self.local_storage.cursor = self.local_storage.connection.cursor()
        return self.local_storage.connection, self.local_storage.cursor

    def close_connection(self):
        # Close the connection at the end of the thread
        if hasattr(self.local_storage, 'connection'):
            self.local_storage.connection.close()

    def create_table(self):
        connection, cursor = self.get_connection()
        cursor.execute("CREATE TABLE IF NOT EXISTS plants (PK INTEGER PRIMARY KEY, name TEXT, water_freq TEXT, fertilizer_freq TEXT, temp_min INTEGER, temp_max INTEGER, humidity_min INTEGER, humidity_max INTEGER)")
        connection.commit()

    def insert_plant(self, name, water_freq, fertilizer_freq, temp_min: int, temp_max: int, humidity_min: int, humidity_max: int):
        connection, cursor = self.get_connection()
        cursor.execute(
            "INSERT INTO plants (name, water_freq, fertilizer_freq, temp_min, temp_max, humidity_min, humidity_max) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (name, water_freq, fertilizer_freq, temp_min, temp_max, humidity_min, humidity_max)
        )
        connection.commit()

    def delete_plant(self, PK: int):
        connection, cursor = self.get_connection()
        local_name = cursor.execute("SELECT name FROM plants WHERE PK=?", (PK,)).fetchone()
        cursor.execute("DELETE FROM plants WHERE PK=?", (PK,))
        connection.commit()

    def update_plant(self, PK: int, column, value):
        if column not in self.COLUMNS:
            raise ValueError(f"Invalid column name: {column}")
        connection, cursor = self.get_connection()
        cursor.execute(f"UPDATE plants SET {column} = ? WHERE PK = ?", (value, PK))
        connection.commit()

    def get_plant(self, PK: int):
        connection, cursor = self.get_connection()
        cursor.execute("SELECT * FROM plants WHERE PK=?", (PK,))
        result = cursor.fetchone()
        return result

    def get_all_plants(self):
        connection, cursor = self.get_connection()
        cursor.execute("SELECT * FROM plants")
        results = cursor.fetchall()
        return results


if __name__ == "__main__":
    garden = Garden()

    try:
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
                print(garden.get_plant(PK))
            elif choice == '5':
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")

    finally:
        garden.close_connection()
