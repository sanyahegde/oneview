"""
Sentiment Analysis Training Script

This script trains a sentiment analysis model on financial headlines
and exports it to Core ML format for use in the iOS app.

IMPORTANT: This model is for educational purposes only.
Do not use for actual trading decisions.
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import coremltools as ct
import pickle
import os
import re
from typing import List, Tuple


def load_financial_headlines(file_path: str) -> pd.DataFrame:
    """Load financial headlines dataset."""
    if not os.path.exists(file_path):
        print(f"Creating mock dataset at {file_path}")
        return create_mock_dataset()
    
    df = pd.read_csv(file_path)
    print(f"Loaded {len(df)} headlines from {file_path}")
    return df


def create_mock_dataset() -> pd.DataFrame:
    """Create a mock dataset for demonstration."""
    headlines = [
        "Apple reports strong quarterly earnings beating expectations",
        "Market volatility concerns investors as stocks decline",
        "Fed signals potential rate cuts to boost economy",
        "Tesla stock surges on positive delivery numbers",
        "Banking sector faces regulatory challenges",
        "Tech stocks rally on positive earnings reports",
        "Economic uncertainty weighs on market sentiment",
        "Oil prices rise on supply concerns",
        "Cryptocurrency market shows signs of recovery",
        "Inflation data shows signs of cooling",
        "Job market remains strong despite economic headwinds",
        "Housing market shows resilience in face of rate hikes",
        "Consumer spending remains robust",
        "Manufacturing sector shows mixed signals",
        "Global supply chain issues continue to impact markets",
        "Energy sector benefits from rising commodity prices",
        "Healthcare stocks gain on positive drug trial results",
        "Retail sector struggles with changing consumer behavior",
        "Financial services face increased regulatory scrutiny",
        "Technology sector leads market gains"
    ]
    
    sentiments = [
        "positive", "negative", "neutral", "positive", "negative",
        "positive", "negative", "positive", "positive", "neutral",
        "positive", "neutral", "positive", "neutral", "negative",
        "positive", "positive", "negative", "negative", "positive"
    ]
    
    df = pd.DataFrame({
        'headline': headlines,
        'sentiment': sentiments
    })
    
    return df


def preprocess_text(text: str) -> str:
    """Preprocess text for sentiment analysis."""
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def prepare_data(df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
    """Prepare data for training."""
    # Preprocess headlines
    df['processed_headline'] = df['headline'].apply(preprocess_text)
    
    # Convert sentiment to numeric labels
    sentiment_map = {'negative': 0, 'neutral': 1, 'positive': 2}
    df['sentiment_label'] = df['sentiment'].map(sentiment_map)
    
    # Vectorize text
    vectorizer = TfidfVectorizer(
        max_features=1000,
        stop_words='english',
        ngram_range=(1, 2)
    )
    
    X = vectorizer.fit_transform(df['processed_headline'])
    y = df['sentiment_label'].values
    
    return X, y, vectorizer


def train_sentiment_model(X: np.ndarray, y: np.ndarray) -> LogisticRegression:
    """Train sentiment analysis model."""
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Train model
    model = LogisticRegression(
        random_state=42,
        max_iter=1000,
        C=1.0
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"Model accuracy: {accuracy:.3f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, 
                              target_names=['negative', 'neutral', 'positive']))
    
    return model


def export_to_coreml(model: LogisticRegression, vectorizer: TfidfVectorizer) -> None:
    """Export model to Core ML format."""
    # Create Core ML model
    coreml_model = ct.converters.sklearn.convert(
        model,
        input_features=[
            ct.models.datatypes.Array(1000)  # TF-IDF vector size
        ],
        output_feature_names=['sentiment']
    )
    
    # Add metadata
    coreml_model.short_description = "Financial news sentiment analysis"
    coreml_model.author = "PortfolioAI Team"
    coreml_model.license = "MIT"
    coreml_model.version = "1.0"
    
    # Save model
    output_path = "../models/sentiment.mlmodel"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    coreml_model.save(output_path)
    
    print(f"Core ML model saved to {output_path}")
    
    # Save vectorizer for preprocessing
    vectorizer_path = "../models/vectorizer.pkl"
    with open(vectorizer_path, 'wb') as f:
        pickle.dump(vectorizer, f)
    
    print(f"Vectorizer saved to {vectorizer_path}")


def main():
    """Main training function."""
    print("Starting sentiment analysis model training...")
    
    # Load data
    data_path = "../data/financial_headlines.csv"
    df = load_financial_headlines(data_path)
    
    # Prepare data
    X, y, vectorizer = prepare_data(df)
    
    # Train model
    model = train_sentiment_model(X, y)
    
    # Export to Core ML
    export_to_coreml(model, vectorizer)
    
    print("Training completed successfully!")
    print("\nIMPORTANT: This model is for educational purposes only.")
    print("Do not use for actual trading decisions.")


if __name__ == "__main__":
    main()
