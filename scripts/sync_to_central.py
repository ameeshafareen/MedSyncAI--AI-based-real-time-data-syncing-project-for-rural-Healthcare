import mysql.connector
from datetime import datetime

# ✅ Replace with your actual freesqldatabase credentials
DB_HOST = "sql12.freesqldatabase.com"
DB_USER = "sql12773852"
DB_PASSWORD = "ZRJWbBEcwW"
DB_NAME = "sql12773852"

# ✅ Sample local records to sync (replace with your actual unsynced data)
unsynced_records = [
    ("Alice", "alice@example.com", "Migraine", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    ("Bob", "bob@example.com", "COVID-19", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
]

def sync_to_central():
    try:
        # Connect to your central MySQL database
        connection = mysql.connector.connect(
            host="sql12.freesqldatabase.com",
            user="sql12773852",
            password="ZRJWbBEcwW",
            database="sql12773852"
        )
        cursor = connection.cursor()
        print("✅ Connected to central database.")

        # Create table if not exists (optional safety)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS synced_records (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                email VARCHAR(255),
                diagnosis VARCHAR(255),
                timestamp DATETIME
            );
        ''')

        # Insert unsynced records
        insert_query = '''
            INSERT INTO synced_records (name, email, diagnosis, timestamp)
            VALUES (%s, %s, %s, %s)
        '''
        cursor.executemany(insert_query, unsynced_records)
        connection.commit()
        print(f"✅ Synced {cursor.rowcount} records to central database.")

    except mysql.connector.Error as err:
        print(f"❌ Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("🔌 Connection closed.")

# 👉 Run this script directly to sync data
if __name__ == "__main__":
    sync_to_central()
