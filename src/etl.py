
import csv
import boto3
from pathlib import Path
from src.s3_reader import get_transactions


file_path = Path(__file__).resolve().parent.parent / "data" / "transactions.csv"


# TRANSFORM
def transform(transactions):
    seen_ids = set()
    valid_transactions = []
    invalid_transactions = []
    flagged_transactions = []

    for row in transactions:
        transaction_id = row["transaction_id"]

        if transaction_id not in seen_ids:
            seen_ids.add(transaction_id)

            if row["amount"] == "":
                invalid_transactions.append(row)
            elif float(row["amount"]) < 0:
                flagged_transactions.append(row)
            else:
                valid_transactions.append(row)

    return valid_transactions, invalid_transactions, flagged_transactions


# LOAD
def load(output_dir):
    session = boto3.Session(
        profile_name="personal",
        region_name="ap-south-1"
    )

    s3 = session.client("s3")
    bucket = "bankflow-data-etl-bucket-002"

    for filename in [
        "valid_transactions.csv",
        "invalid_transactions.csv",
        "flagged_transactions.csv"
    ]:
        local_path = output_dir / filename

        s3_key = (
            f"processed/{filename}"
            if filename.startswith("valid")
            else f"flagged/{filename}"
            if filename.startswith("flagged")
            else f"invalid/{filename}"
        )

        s3.upload_file(str(local_path), bucket, s3_key)
        print(f"Uploaded: {s3_key}")


# MAIN PIPELINE
def main():
    transactions = get_transactions()

    valid_transactions, invalid_transactions, flagged_transactions = transform(transactions)

    print("Valid transactions:", len(valid_transactions))
    print("Invalid transactions:", len(invalid_transactions))
    print("Flagged transactions:", len(flagged_transactions))

    output_dir = file_path.parent / "processed"
    output_dir.mkdir(exist_ok=True)

    fieldnames = list(transactions[0].keys())

    for filename, records in [
        ("valid_transactions.csv", valid_transactions),
        ("invalid_transactions.csv", invalid_transactions),
        ("flagged_transactions.csv", flagged_transactions),
    ]:
        with open(output_dir / filename, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(records)

    load(output_dir)


if __name__ == "__main__":
    main()
