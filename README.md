# FRED-Economic-Data-Pipeline
Python data pipeline that fetches time-series data from the FRED API (Federal Reserve Economic Data), processes it, and visualises relationships between key economic indicators (e.g., inflation vs. unemployment) using Matplotlib or Seaborn.

This project provides a professional, scalable solution for reliable data ingestion from the Federal Reserve Economic Data (FRED) source. It serves as the foundation layer for macroeconomic time series analysis, forecasting, and quantitative research.

The pipeline is engineered to ensure data consistency, minimise latency in retrieval, and deliver normalised, analysis-ready datasets directly to downstream modelling environments.

I. Problem Statement and Solution

The Challenge: Economic time series data often requires manual collection, key management, non-standardised formats, and complex handling of varying observation frequencies (e.g., daily, monthly, quarterly). This slows down the research lifecycle.

The Solution: This pipeline automates the entire Extract, Transform, and Load (ETL) process for designated economic indicators. It guarantees that the research team always operates on a single source of truth that is programmatically updated.

II. System Architecture and Dependencies

Data Flow

Extraction: Secure connection to the FRED API using the provided API key.

Transformation: Data is retrieved in raw JSON/XML, converted to a Pandas DataFrame, and standardised (e.g., date indexing, series ID column naming).

Normalisation: Time series data is processed to handle missing observations and, where necessary, adjusted for frequency alignment (e.g., down-sampling high-frequency data for a quarterly model).

Load: The final dataset is persisted to a designated local file path for immediate use.

Prerequisites

Python 3.8+

FRED API Key: A valid key is mandatory for authentication.

Setup and Configuration

Clone the Repository:

git clone [https://github.com/Rishita0613/FRED-Economic-Data-Pipeline.git](https://github.com/Rishita0613/FRED-Economic-Data-Pipeline.git)
cd FRED-Economic-Data-Pipeline


Install Environment:

pip install -r requirements.txt


Environment Variable: For secure operation, the API key must be exported as an environment variable before execution.

export FRED_API_KEY="YOUR_SECRET_KEY"


III. Execution and Output

Execution Command

The pipeline is executed via the primary script. The configuration of specific FRED Series IDs (e.g., GDP, CPIAUCSL, FEDFUNDS) is handled internally by this script.

python run_pipeline.py


Analytical Output

The successful execution generates a file named economic_indicators.csv (or a similar file type like .parquet for better efficiency).


This output file is the sole input required for subsequent data science tasks, including econometric modelling, dashboard visualisation, and machine learning forecasting.
