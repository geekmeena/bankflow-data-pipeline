
from datetime import datetime, timedelta
from airflow.sdk import dag, task


@dag(
    dag_id="bankflow_pipeline",
    start_date=datetime(2026, 11, 1),
    schedule="0 9 * * *",
    catchup=False,
    default_args={
        "retries": 2,
        "retry_delay": timedelta(minutes=1),
    },
    tags=["bankflow"],
)
def bankflow_pipeline():

    @task
    def extract():
        import sys
        sys.path.insert(0, "/opt/airflow/bankflow")

        from src.s3_reader import get_transactions

        transactions = get_transactions()

        print(f"Extracted {len(transactions)} transactions from S3")
        return transactions

    @task
    def transform(transactions):
        import sys
        sys.path.insert(0, "/opt/airflow/bankflow")

        from src.etl import transform as clean_data

        valid, invalid, flagged = clean_data(transactions)

        print(f"Valid transactions: {len(valid)}")
        print(f"Invalid transactions: {len(invalid)}")
        print(f"Flagged transactions: {len(flagged)}")

        return {
            "valid": valid,
            "invalid": invalid,
            "flagged": flagged,
        }

    @task
    def load(cleaned_data):
        from airflow.providers.postgres.hooks.postgres import PostgresHook

        hook = PostgresHook(postgres_conn_id="bankflow_postgres")

        valid_transactions = cleaned_data["valid"]

        sql = """
            INSERT INTO transactions
            (transaction_id, customer_id, date, amount,
             currency, transaction_type, category)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (transaction_id) DO NOTHING
        """

        for row in valid_transactions:
            hook.run(
                sql,
                parameters=(
                    row["transaction_id"],
                    row["customer_id"],
                    row["date"],
                    row["amount"],
                    row["currency"],
                    row["transaction_type"],
                    row["category"],
                ),
            )

        print(f"Processed {len(valid_transactions)} valid transactions for PostgreSQL")

    @task
    def test_dbt_connection():
        import os
        import subprocess
        from airflow.providers.postgres.hooks.postgres import PostgresHook

        conn = PostgresHook(
            postgres_conn_id="bankflow_postgres"
        ).get_connection("bankflow_postgres")

        env = os.environ.copy()
        env["DBT_LOG_PATH"] = "/tmp/bankflow_dbt_logs"
        env["DBT_TARGET_PATH"] = "/tmp/bankflow_dbt_target"
        env["DB_USER"] = conn.login
        env["DB_PASSWORD"] = conn.password
        env["DBT_ENGINE_MANAGE_STATE"] = "false"

        subprocess.run(
            [
                "dbt",
                "build",
                "--select",
                "customer_spending",
                "--project-dir",
                "/opt/airflow/bankflow/dbt",
            ],
            env=env,
            check=True,
        )

    # Define task order
    extracted_data = extract()
    cleaned_data = transform(extracted_data)
    load_task = load(cleaned_data)
    dbt_task = test_dbt_connection()

    load_task >> dbt_task


bankflow_pipeline()
