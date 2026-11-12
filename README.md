# BankFlow — AWS Cloud ETL Data Pipeline

## Overview
BankFlow is a cloud-based banking data pipeline built using Python and AWS S3. It processes synthetic banking transactions, removes duplicates, identifies missing amounts, and separates valid and invalid records.

## Technologies
- Python
- AWS S3
- Boto3
- Pytest
- Git & GitHub

## Architecture

Raw CSV → AWS S3 → Python ETL → AWS S3 (Processed / Invalid)

## ETL Process

1. **Extract:** Read raw banking transactions from AWS S3 using Boto3.
2. **Transform:** Remove duplicate transactions and separate records with missing amounts.
3. **Load:** Save the processed files locally and upload them to AWS S3.

## Testing

Pytest is used to verify:
- Duplicate transaction removal
- Missing amount detection

Run tests:

`python -m pytest tests/ -v`

## Running the Pipeline

Install dependencies:

`pip install -r requirements.txt`

Configure an AWS profile with access to the S3 bucket, then run:

`python -m src.etl`

## Current Results

Using 11 synthetic banking records:

- 9 valid transactions
- 1 invalid transaction
- 1 duplicate removed

## Future Improvements

- SQL and PostgreSQL
- Apache Airflow and dbt
- Data quality validation
- Terraform and GitHub Actions
- Dashboard and AI data assistant

## Project Status

Phase 1: Python ETL — Completed

Phase 2: AWS S3 Integration — Completed

Automated testing — Initial tests completed

Further development is in progress.
