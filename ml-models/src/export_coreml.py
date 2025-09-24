"""
Core ML Export Script

This script exports trained models to Core ML format for use in iOS apps.
"""

import coremltools as ct
import pickle
import os
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


def export_sentiment_model():
    """Export sentiment analysis model to Core ML."""
    print("Exporting sentiment analysis model...")
    
    # Check if model files exist
    model_path = "../models/sentiment_model.pkl"
    vectorizer_path = "../models/vectorizer.pkl"
    
    if not os.path.exists(model_path) or not os.path.exists(vectorizer_path):
        print("Model files not found. Please run train_sentiment.py first.")
        return
    
    # Load model and vectorizer
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    with open(vectorizer_path, 'rb') as f:
        vectorizer = pickle.load(f)
    
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
    
    # Add input description
    coreml_model.input_description['input'] = "TF-IDF vectorized text features"
    
    # Add output description
    coreml_model.output_description['sentiment'] = "Sentiment prediction (0: negative, 1: neutral, 2: positive)"
    
    # Save model
    output_path = "../models/sentiment.mlmodel"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    coreml_model.save(output_path)
    
    print(f"Sentiment model exported to {output_path}")


def create_mock_sentiment_model():
    """Create a mock sentiment model for demonstration."""
    print("Creating mock sentiment model...")
    
    # Create a simple mock model
    from sklearn.linear_model import LogisticRegression
    from sklearn.feature_extraction.text import TfidfVectorizer
    
    # Mock training data
    texts = [
        "Apple reports strong earnings",
        "Market volatility concerns investors",
        "Fed signals rate cuts",
        "Tesla stock surges",
        "Banking sector faces challenges"
    ]
    
    labels = [2, 0, 1, 2, 0]  # positive, negative, neutral, positive, negative
    
    # Train simple model
    vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
    X = vectorizer.fit_transform(texts)
    
    model = LogisticRegression(random_state=42)
    model.fit(X, labels)
    
    # Export to Core ML
    coreml_model = ct.converters.sklearn.convert(
        model,
        input_features=[
            ct.models.datatypes.Array(1000)
        ],
        output_feature_names=['sentiment']
    )
    
    # Add metadata
    coreml_model.short_description = "Financial news sentiment analysis (Mock)"
    coreml_model.author = "PortfolioAI Team"
    coreml_model.license = "MIT"
    coreml_model.version = "1.0"
    
    # Save model
    output_path = "../models/sentiment.mlmodel"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    coreml_model.save(output_path)
    
    print(f"Mock sentiment model exported to {output_path}")


def create_mock_price_signal_model():
    """Create a mock price signal model for demonstration."""
    print("Creating mock price signal model...")
    
    # Create a simple mock model
    from sklearn.ensemble import RandomForestClassifier
    
    # Mock training data
    np.random.seed(42)
    X = np.random.rand(100, 10)  # 100 samples, 10 features
    y = np.random.randint(0, 2, 100)  # Binary classification
    
    # Train simple model
    model = RandomForestClassifier(n_estimators=10, random_state=42)
    model.fit(X, y)
    
    # Export to Core ML
    coreml_model = ct.converters.sklearn.convert(
        model,
        input_features=[
            ct.models.datatypes.Array(10)
        ],
        output_feature_names=['signal']
    )
    
    # Add metadata
    coreml_model.short_description = "Price signal prediction (Mock)"
    coreml_model.author = "PortfolioAI Team"
    coreml_model.license = "MIT"
    coreml_model.version = "1.0"
    
    # Save model
    output_path = "../models/price_signal.mlmodel"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    coreml_model.save(output_path)
    
    print(f"Mock price signal model exported to {output_path}")


def verify_models():
    """Verify that exported models can be loaded."""
    print("Verifying exported models...")
    
    # Check sentiment model
    sentiment_path = "../models/sentiment.mlmodel"
    if os.path.exists(sentiment_path):
        try:
            model = ct.models.MLModel(sentiment_path)
            print(f"✓ Sentiment model loaded successfully")
            print(f"  Input: {model.input_description}")
            print(f"  Output: {model.output_description}")
        except Exception as e:
            print(f"✗ Error loading sentiment model: {e}")
    else:
        print("✗ Sentiment model not found")
    
    # Check price signal model
    price_signal_path = "../models/price_signal.mlmodel"
    if os.path.exists(price_signal_path):
        try:
            model = ct.models.MLModel(price_signal_path)
            print(f"✓ Price signal model loaded successfully")
            print(f"  Input: {model.input_description}")
            print(f"  Output: {model.output_description}")
        except Exception as e:
            print(f"✗ Error loading price signal model: {e}")
    else:
        print("✗ Price signal model not found")


def main():
    """Main export function."""
    print("Starting Core ML model export...")
    
    # Create models directory
    os.makedirs("../models", exist_ok=True)
    
    # Export models (create mock versions if training files don't exist)
    try:
        export_sentiment_model()
    except:
        create_mock_sentiment_model()
    
    create_mock_price_signal_model()
    
    # Verify models
    verify_models()
    
    print("\nCore ML export completed!")
    print("Models are ready for use in the iOS app.")
    print("\nIMPORTANT: These models are for educational purposes only.")
    print("Do not use for actual trading decisions.")


if __name__ == "__main__":
    main()
