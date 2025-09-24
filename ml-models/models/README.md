# ML Models

This directory contains machine learning models for sentiment analysis and price signal prediction.

## Models

- `sentiment.mlmodel` - Core ML model for financial news sentiment analysis
- `price_signal.mlmodel` - Core ML model for price signal prediction

## Training Scripts

- `train_sentiment.py` - Trains sentiment analysis model
- `train_price_signal.py` - Trains price signal prediction model
- `export_coreml.py` - Exports trained models to Core ML format

## Data

Place your training data in the `data/` directory:
- `financial_headlines.csv` - Headlines with sentiment labels
- `stock_prices.csv` - Historical stock price data

## Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Train sentiment model:
   ```bash
   python train_sentiment.py
   ```

3. Train price signal model:
   ```bash
   python train_price_signal.py
   ```

4. Export to Core ML:
   ```bash
   python export_coreml.py
   ```

## Important Notice

**These models are for educational purposes only and should not be used for actual trading decisions.**
