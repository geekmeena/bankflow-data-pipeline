import psycopg2
import os
import csv
from pathlib import Path

connection = psycopg2.connect(
    host="localhost",
    database="bankflow_db",
    user="meena",
    password=os.environ["DB_PASSWORD"],
    port=5432
)

print("Connected to PostgreSQL successfully!")

file_path = Path("data/processed/valid_transactions.csv")

with open(file_path, "r") as file:
    reader = csv.DictReader(file)

    cursor = connection.cursor()

    for row in reader:
        cursor.execute(
            """
            INSERT INTO transactions
            (transaction_id, customer_id, date, amount,
             currency, transaction_type, category)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (transaction_id) DO NOTHING
            """,
            (
                row["transaction_id"],
                row["customer_id"],
                row["date"],
                row["amount"],
                row["currency"],
                row["transaction_type"],
                row["category"],
            )
        )

    connection.commit()
    cursor.close()

print("Transactions loaded successfully!")

connection.close()