# Data Directory

This directory contains training data for the ML models.

## Required Files

### Financial Headlines Dataset
- **File**: `financial_headlines.csv`
- **Format**: CSV with columns: `headline`, `sentiment`
- **Sentiment values**: `positive`, `negative`, `neutral`
- **Example**:
  ```csv
  headline,sentiment
  "Apple reports strong quarterly earnings",positive
  "Market volatility concerns investors",negative
  "Fed signals potential rate cuts",neutral
  ```

### Stock Price Dataset
- **File**: `stock_prices.csv`
- **Format**: CSV with columns: `symbol`, `date`, `open`, `high`, `low`, `close`, `volume`
- **Example**:
  ```csv
  symbol,date,open,high,low,close,volume
  AAPL,2024-01-01,150.0,155.0,149.0,154.0,1000000
  ```

## Data Sources

You can obtain training data from:

1. **Financial News APIs**:
   - Alpha Vantage News API
   - NewsAPI
   - Financial Modeling Prep

2. **Stock Price APIs**:
   - Alpha Vantage
   - Yahoo Finance (yfinance)
   - IEX Cloud

3. **Kaggle Datasets**:
   - Financial news sentiment datasets
   - Stock price datasets

## Data Preparation

1. Download or collect your data
2. Place CSV files in this directory
3. Ensure data is clean and properly formatted
4. Run training scripts to process the data

## Privacy Notice

- Only use publicly available data
- Do not include personal or confidential information
- Respect data source terms of service
- Consider data licensing requirements
