import csv
import sqlite3
import os

def create_table(cursor):
    """
    Create the detections table in the SQLite database
    """
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS detections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        class TEXT,
        timestamp TEXT,
        frame INTEGER,
        bounding_box_coord0 REAL,
        bounding_box_coord1 REAL,
        bounding_box_coord2 REAL,
        bounding_box_coord3 REAL,
        confidence REAL
    )
    ''')

def insert_data(cursor, data):
    """
    Insert data into the detections table
    """
    cursor.execute('''
    INSERT INTO detections (class, timestamp, frame, bounding_box_coord0, bounding_box_coord1, bounding_box_coord2, bounding_box_coord3, confidence)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', data)

def main():
    db_file = 'detections.db'
    csv_file = os.path.join('output', 'detection_results.csv')
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    create_table(cursor)
    
    # Read CSV and insert data into the database
    with open(csv_file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row as it contains metadata only
        for row in reader:
            insert_data(cursor, row)
    
    conn.commit()
    conn.close()
    print(f"Data from {csv_file} has been successfully inserted into {db_file}")

if __name__ == "__main__":
    main()
