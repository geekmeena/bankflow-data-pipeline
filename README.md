# BankFlow — AWS Cloud ETL Data Pipeline

## Overview

BankFlow is a cloud-based data engineering project that processes synthetic banking transactions using Python, AWS S3, PostgreSQL and Apache Airflow.

The pipeline extracts raw transaction data, removes duplicates, identifies invalid and flagged transactions, and loads valid records into PostgreSQL for analysis.

Apache Airflow orchestrates the pipeline and provides scheduling, retries and execution monitoring.

## Technologies

- **Python** — ETL processing and data validation
- **AWS S3** — Raw and processed data storage
- **Boto3** — AWS integration
- **PostgreSQL** — Structured transaction storage
- **SQL** — Transaction analysis
- **Apache Airflow** — Workflow orchestration and scheduling
- **Docker Compose** — Local Airflow environment
- **Pytest** — Automated testing
- **Git & GitHub** — Version control

## Architecture

Raw Banking CSV → AWS S3 → Apache Airflow → Python ETL → PostgreSQL → SQL Analysis

The standalone ETL script also saves processed, invalid and flagged transaction files to AWS S3.

## ETL Process

1. **Extract:** Retrieve raw banking transactions from AWS S3 using Boto3.
2. **Transform:** Remove duplicate transaction IDs, identify missing amounts and flag negative amounts.
3. **Load:** Insert valid transactions into PostgreSQL using an Airflow PostgreSQL connection.

## Data Quality

The pipeline separates transactions into three categories:

- **Valid:** Records passing the current validation rules.
- **Invalid:** Records with missing amounts.
- **Flagged:** Records containing negative amounts requiring investigation.

PostgreSQL uses `ON CONFLICT DO NOTHING` to prevent duplicate transaction IDs during repeated pipeline runs.

## Apache Airflow

Airflow orchestrates three tasks:

Extract → Transform → Load

The DAG includes:

- Daily scheduling at 09:00 UTC
- Two retries with a one-minute delay
- `catchup=False`
- Task execution logs and monitoring
- PostgreSQL connection management

## Testing

Three Pytest tests verify:

- Duplicate transaction removal
- Missing amount detection
- Negative amount flagging

Run the tests:

`python -m pytest tests/ -v`

## Current Results

Using 12 synthetic banking records:

| Result | Count |
|---|---:|
| Valid transactions | 9 |
| Invalid transactions | 1 |
| Flagged transactions | 1 |
| Duplicate records removed | 1 |
| Records stored in PostgreSQL | 9 |

All three automated tests passed.

## Running Locally

Install Python dependencies:

`pip install -r requirements.txt`

Configure your AWS credentials and PostgreSQL connection.

Run the standalone ETL pipeline:

`python -m src.etl`

Start the Airflow environment:

`cd airflow`

`docker compose up -d`

Open the Airflow dashboard at `http://localhost:8080` and access the `bankflow_pipeline` DAG.

**Note:** The current setup uses local development configuration, an AWS profile and a locally hosted PostgreSQL database. Additional configuration is required when running on another machine.

## Future Improvements

- dbt for SQL transformations
- Expanded data-quality checks
- Terraform for infrastructure provisioning
- GitHub Actions for CI/CD
- Data analytics dashboard
- LLM-powered data analysis assistant

## Project Status

- Python ETL — Completed
- AWS S3 integration — Completed
- PostgreSQL and SQL analysis — Completed
- Airflow orchestration — Completed
- Initial automated data-quality checks — Completed
- Further development — In progress

*This project uses synthetic banking transactions for educational and portfolio purposes.*