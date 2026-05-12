# Rates Data Pipeline

## Overview
Automated ETL pipeline that ingests benchmark interest rates (SOFR, 10Y Treasury, 2Y Treasury) from the Federal Reserve Economic Data (FRED) API and stores them in PostgreSQL for analysis.

## Why This Matters
- SOFR is the primary benchmark rate for $200+ trillion in financial contracts
- Yield curve analysis (2Y vs 10Y spread) is a leading recession indicator
- Trading desks and risk teams rely on clean, validated rate data

## Architecture
- **Extract:** Python requests library hits FRED API
- **Transform:** Data cleaning, type conversion, missing value handling
- **Load:** PostgreSQL with upsert logic (handles duplicates)

## Tech Stack
- Python 3.x
- PostgreSQL
- FRED API
- psycopg2, requests, python-dotenv

## Data Quality
- Filters missing values ("." entries)
- Validates trading day calendar
- Upsert logic prevents duplicates

## Setup
1. Clone repo
2. Create `.env` file with credentials
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `python app.py`

## Database Schema
TBC

## Future Enhancements
- Add data validation layer (weekend/holiday checks)
- Calculate yield curve spread and inversion detection
- Add automated scheduling (daily updates)
- Build analytics dashboard
