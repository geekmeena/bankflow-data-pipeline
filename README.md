BankFlow — AWS Cloud ETL Data Pipeline
Overview
BankFlow is a data engineering portfolio project that processes synthetic banking transactions using Python, AWS S3, PostgreSQL, Apache Airflow, and dbt.

The pipeline reads raw transaction data from S3, removes duplicates, separates invalid or flagged records, loads valid transactions into PostgreSQL, and builds a customer-spending summary with dbt. Airflow schedules and monitors the workflow.
Technologies
- Python — ETL processing and validation
- AWS S3 — Raw data storage; processed, invalid, and flagged outputs from the standalone ETL script
- Boto3 — AWS S3 integration
- PostgreSQL — Transaction storage and SQL analytics
- Apache Airflow 3 — Workflow orchestration, scheduling, retries, and logs
- dbt Core / dbt-postgres — SQL transformations and data tests
- Docker Compose — Local Airflow environment with a custom image containing dbt
- Pytest — Python ETL tests
- Git & GitHub — Version control
Architecture
Synthetic transaction CSV
         |
         v
       AWS S3
         |
         v
    Apache Airflow
         |
   Extract (Python)
         |
  Transform (Python)
         |
  Load valid records
         |
     PostgreSQL
         |
    dbt build
         |
 customer_spending view
    + dbt data tests
The standalone Python ETL script can also write valid, invalid, and flagged CSV files to separate S3 prefixes.
ETL and Data Quality
1. Extract: Read raw transactions from S3 using Boto3.
2. Transform: Remove duplicate transaction IDs; separate records with missing amounts and flag negative amounts.
3. Load: Insert valid records into PostgreSQL using an Airflow-managed database connection.
4. Model and test: Use dbt to create the dbt_dev.customer_spending view and test its customer_id column for not_null and unique values.
PostgreSQL inserts use ON CONFLICT (transaction_id) DO NOTHING to avoid duplicate inserts when the pipeline is rerun.

These are introductory validation rules for a synthetic dataset, not a production fraud-detection system.
Apache Airflow
The bankflow_pipeline DAG runs the tasks in this order:
extract → transform → load → test_dbt_connection
The final task is currently named test_dbt_connection, but its command has been updated to dbt build --select customer_spending, so it builds the model and runs its associated tests.
- Schedule: Daily at 09:00 UTC
- Retries: Two retries, one minute apart
- Catchup: Disabled
- Monitoring: Airflow task logs and run status
- Database credentials: Obtained from an Airflow connection at task runtime, not embedded in the DAG
dbt Transformation and Tests
The customer_spending model sums debit transaction amounts by customer from public.transactions and creates the view dbt_dev.customer_spending.

Successful Airflow dbt build:
Check	Result
customer_spending SQL view	Passed
customer_id not null	Passed
customer_id unique	Passed
Total	3 passed, 0 errors


Python Tests
Three Pytest tests cover duplicate removal, missing amount detection, and negative amount flagging.
python -m pytest tests/ -v
Demonstration Results
The current example contains 12 synthetic source records.
Result	Count
Valid transactions	9
Invalid transactions (missing amount)	1
Flagged transactions (negative amount)	1
Duplicate transactions removed	1
Transactions stored in PostgreSQL	9


The latest Airflow run completed the dbt model and its two data tests successfully.
Running Locally
This project has been tested with local PostgreSQL and Airflow running in Docker Compose. Running it on another machine requires local configuration.
1. Create a Python virtual environment and install project dependencies:
   pip install -r requirements.txt
2. Configure AWS credentials locally, create the required S3 bucket and upload the synthetic transaction CSV. Configure a local PostgreSQL database and the transaction table.
3. Run the standalone ETL pipeline if desired:
   python -m src.etl
4. Start Airflow (the custom image installs dbt):
   cd airflow
   docker compose --parallel 1 build
   docker compose up -d --no-build
5. Open http://localhost:8080, configure the Airflow PostgreSQL connection bankflow_postgres, and trigger bankflow_pipeline.
The local Docker setup mounts the dbt project read-only. dbt log and target output directories are redirected to writable temporary paths inside the container.
Configuration note: The setup currently uses a local AWS profile, a developer-managed PostgreSQL instance, and Docker networking (host.docker.internal). It is not a one-command production deployment.

Security Notes
- Use synthetic data only; do not upload real customer banking information.
- Keep AWS access keys, database passwords, and other credentials out of Git.
- Keep local .env files and AWS credentials files untracked.
- dbt's profiles.yml uses environment-variable references for database credentials rather than hard-coded secrets.
- Airflow's dbt task obtains credentials from the Airflow PostgreSQL connection at runtime.
- Review git status and staged files before pushing changes.
Future Improvements
- Expand Python and dbt data-quality checks
- Provision AWS resources with Terraform
- Add GitHub Actions for automated testing and CI/CD
- Add a transaction analytics dashboard
- Explore an optional LLM-powered data analysis assistant
Project Status
Component	Status
Python ETL and AWS S3	Complete
PostgreSQL storage and SQL analysis	Complete
Airflow orchestration	Complete
Python ETL unit tests	Complete
dbt model and automated dbt tests in Airflow	Complete
Terraform, CI/CD, and dashboard	Planned


BankFlow uses synthetic banking transactions for learning and portfolio demonstration purposes.