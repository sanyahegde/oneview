"""
Price Signal Training Script

This script trains a price signal prediction model using historical stock data
and exports metrics for analysis.

IMPORTANT: This model is for educational purposes only.
Do not use for actual trading decisions.
"""

import pandas as pd
import numpy as np
import yfinance as yf
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
import os
from typing import List, Tuple
from datetime import datetime, timedelta


def download_stock_data(symbol: str, period: str = "2y") -> pd.DataFrame:
    """Download stock data using yfinance."""
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period=period)
        data['Symbol'] = symbol
        return data
    except Exception as e:
        print(f"Error downloading data for {symbol}: {e}")
        return pd.DataFrame()


def create_mock_data() -> pd.DataFrame:
    """Create mock stock data for demonstration."""
    dates = pd.date_range(start='2022-01-01', end='2024-01-01', freq='D')
    np.random.seed(42)
    
    # Generate realistic price movements
    prices = [100]
    for _ in range(len(dates) - 1):
        change = np.random.normal(0, 0.02)  # 2% daily volatility
        new_price = prices[-1] * (1 + change)
        prices.append(max(new_price, 1))  # Ensure positive prices
    
    data = pd.DataFrame({
        'Date': dates,
        'Open': prices,
        'High': [p * (1 + abs(np.random.normal(0, 0.01))) for p in prices],
        'Low': [p * (1 - abs(np.random.normal(0, 0.01))) for p in prices],
        'Close': prices,
        'Volume': np.random.randint(1000000, 10000000, len(dates)),
        'Symbol': 'MOCK'
    })
    
    data.set_index('Date', inplace=True)
    return data


def calculate_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate technical indicators for price signal prediction."""
    data = df.copy()
    
    # Moving averages
    data['MA_5'] = data['Close'].rolling(window=5).mean()
    data['MA_20'] = data['Close'].rolling(window=20).mean()
    data['MA_50'] = data['Close'].rolling(window=50).mean()
    
    # Price momentum
    data['Momentum_5'] = data['Close'] / data['Close'].shift(5) - 1
    data['Momentum_10'] = data['Close'] / data['Close'].shift(10) - 1
    
    # Volatility
    data['Volatility_10'] = data['Close'].rolling(window=10).std()
    data['Volatility_20'] = data['Close'].rolling(window=20).std()
    
    # RSI (simplified)
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))
    
    # Price position relative to moving averages
    data['Price_vs_MA5'] = (data['Close'] - data['MA_5']) / data['MA_5']
    data['Price_vs_MA20'] = (data['Close'] - data['MA_20']) / data['MA_20']
    data['Price_vs_MA50'] = (data['Close'] - data['MA_50']) / data['MA_50']
    
    # Volume indicators
    data['Volume_MA'] = data['Volume'].rolling(window=20).mean()
    data['Volume_Ratio'] = data['Volume'] / data['Volume_MA']
    
    return data


def create_price_signals(df: pd.DataFrame, lookforward: int = 5) -> pd.DataFrame:
    """Create price signals based on future price movements."""
    data = df.copy()
    
    # Calculate future returns
    data['Future_Return'] = data['Close'].shift(-lookforward) / data['Close'] - 1
    
    # Create signal based on future returns
    # 1: Buy signal (positive return), 0: Hold/Sell signal
    data['Signal'] = (data['Future_Return'] > 0.02).astype(int)  # 2% threshold
    
    return data


def prepare_features(df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
    """Prepare features for training."""
    # Select feature columns
    feature_cols = [
        'MA_5', 'MA_20', 'MA_50',
        'Momentum_5', 'Momentum_10',
        'Volatility_10', 'Volatility_20',
        'RSI',
        'Price_vs_MA5', 'Price_vs_MA20', 'Price_vs_MA50',
        'Volume_Ratio'
    ]
    
    # Remove rows with NaN values
    data_clean = df[feature_cols + ['Signal']].dropna()
    
    X = data_clean[feature_cols].values
    y = data_clean['Signal'].values
    
    return X, y


def train_price_signal_model(X: np.ndarray, y: np.ndarray) -> RandomForestClassifier:
    """Train price signal prediction model."""
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Train model
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        max_depth=10,
        min_samples_split=5
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"Model accuracy: {accuracy:.3f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Hold/Sell', 'Buy']))
    
    # Feature importance
    feature_names = [
        'MA_5', 'MA_20', 'MA_50',
        'Momentum_5', 'Momentum_10',
        'Volatility_10', 'Volatility_20',
        'RSI',
        'Price_vs_MA5', 'Price_vs_MA20', 'Price_vs_MA50',
        'Volume_Ratio'
    ]
    
    feature_importance = pd.DataFrame({
        'feature': feature_names,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\nFeature Importance:")
    print(feature_importance)
    
    return model


def plot_results(df: pd.DataFrame, model: RandomForestClassifier) -> None:
    """Plot analysis results."""
    # Create plots directory
    os.makedirs("../models/plots", exist_ok=True)
    
    # Plot 1: Price and Moving Averages
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['Close'], label='Close Price', alpha=0.7)
    plt.plot(df.index, df['MA_20'], label='MA 20', alpha=0.7)
    plt.plot(df.index, df['MA_50'], label='MA 50', alpha=0.7)
    plt.title('Stock Price and Moving Averages')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('../models/plots/price_ma.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Plot 2: RSI
    plt.figure(figsize=(12, 4))
    plt.plot(df.index, df['RSI'], label='RSI', color='purple')
    plt.axhline(y=70, color='r', linestyle='--', alpha=0.7, label='Overbought')
    plt.axhline(y=30, color='g', linestyle='--', alpha=0.7, label='Oversold')
    plt.title('Relative Strength Index (RSI)')
    plt.xlabel('Date')
    plt.ylabel('RSI')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('../models/plots/rsi.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Plots saved to ../models/plots/")


def export_metrics(model: RandomForestClassifier, df: pd.DataFrame) -> None:
    """Export model metrics and analysis."""
    os.makedirs("../models", exist_ok=True)
    
    # Calculate additional metrics
    total_signals = len(df.dropna())
    buy_signals = df['Signal'].sum()
    signal_rate = buy_signals / total_signals
    
    metrics = {
        'model_type': 'RandomForestClassifier',
        'total_samples': total_signals,
        'buy_signals': int(buy_signals),
        'signal_rate': signal_rate,
        'feature_count': len(model.feature_importances_),
        'training_date': datetime.now().isoformat()
    }
    
    # Save metrics
    import json
    with open('../models/price_signal_metrics.json', 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print("Metrics saved to ../models/price_signal_metrics.json")


def main():
    """Main training function."""
    print("Starting price signal model training...")
    
    # Load or create data
    data_path = "../data/stock_prices.csv"
    if os.path.exists(data_path):
        print(f"Loading data from {data_path}")
        df = pd.read_csv(data_path, index_col=0, parse_dates=True)
    else:
        print("Creating mock stock data...")
        df = create_mock_data()
    
    print(f"Loaded {len(df)} data points")
    
    # Calculate technical indicators
    df = calculate_technical_indicators(df)
    
    # Create price signals
    df = create_price_signals(df)
    
    # Prepare features
    X, y = prepare_features(df)
    
    # Train model
    model = train_price_signal_model(X, y)
    
    # Plot results
    plot_results(df, model)
    
    # Export metrics
    export_metrics(model, df)
    
    print("Training completed successfully!")
    print("\nIMPORTANT: This model is for educational purposes only.")
    print("Do not use for actual trading decisions.")


if __name__ == "__main__":
    main()
