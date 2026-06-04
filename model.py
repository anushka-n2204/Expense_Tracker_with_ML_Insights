"""
ML Model module for expense categorization
Uses TF-IDF vectorization with Logistic Regression
"""
import pickle
import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from typing import Tuple


class ExpenseCategorizer:
    def __init__(self, model_path: str = "models/categorizer.pkl"):
        """Initialize the categorizer"""
        self.model_path = model_path
        self.model = None
        self.categories = [
            "Food", "Transport", "Shopping", "Utilities", 
            "Health", "Entertainment", "Education", "Other"
        ]
        
        # Load model if it exists
        if os.path.exists(model_path):
            self.load_model()
    
    def train(self, training_data_path: str) -> Tuple[float, dict]:
        """
        Train the categorization model
        
        Args:
            training_data_path: Path to CSV file with 'description' and 'category' columns
            
        Returns:
            Tuple of (accuracy, classification_report)
        """
        # Load training data
        df = pd.read_csv(training_data_path)
        
        if 'description' not in df.columns or 'category' not in df.columns:
            raise ValueError("Training data must have 'description' and 'category' columns")
        
        X = df['description']
        y = df['category']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Create pipeline with TF-IDF and Logistic Regression
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=500, ngram_range=(1, 2), lowercase=True)),
            ('classifier', LogisticRegression(max_iter=1000, random_state=42))
        ])
        
        # Train model
        self.model.fit(X_train, y_train)
        
        # Evaluate
        accuracy = self.model.score(X_test, y_test)
        
        # Get predictions for classification report
        from sklearn.metrics import classification_report
        y_pred = self.model.predict(X_test)
        report = classification_report(y_test, y_pred, output_dict=True)
        
        # Save model
        self.save_model()
        
        return accuracy, report
    
    def predict(self, description: str) -> str:
        """
        Predict category for a given expense description
        
        Args:
            description: Expense description text
            
        Returns:
            Predicted category
        """
        if self.model is None:
            # Return default category if model not trained
            return "Other"
        
        prediction = self.model.predict([description])[0]
        return prediction
    
    def predict_proba(self, description: str) -> dict:
        """
        Get prediction probabilities for all categories
        
        Args:
            description: Expense description text
            
        Returns:
            Dictionary of category: probability
        """
        if self.model is None:
            return {cat: 1.0/len(self.categories) for cat in self.categories}
        
        probabilities = self.model.predict_proba([description])[0]
        classes = self.model.classes_
        
        return dict(zip(classes, probabilities))
    
    def save_model(self):
        """Save the trained model to disk"""
        if self.model is not None:
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            with open(self.model_path, 'wb') as f:
                pickle.dump(self.model, f)
    
    def load_model(self):
        """Load a trained model from disk"""
        if os.path.exists(self.model_path):
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
        else:
            self.model = None
    
    def is_trained(self) -> bool:
        """Check if model is trained and loaded"""
        return self.model is not None
