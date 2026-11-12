import boto3
import csv
import io

def get_transactions():
    session = boto3.Session(
        profile_name="personal",
        region_name="ap-south-1"
    )
    s3 = session.client("s3")

    response = s3.get_object(
        Bucket="bankflow-data-etl-bucket-002",
        Key="raw/transactions.csv"
    )

    content = response["Body"].read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(content))

    return list(reader)

