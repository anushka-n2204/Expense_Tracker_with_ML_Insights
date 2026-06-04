"""
Anomaly Detection module using Isolation Forest
Detects unusual spending patterns
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder
from typing import List


class AnomalyDetector:
    def __init__(self, contamination: float = 0.05):
        """
        Initialize anomaly detector
        
        Args:
            contamination: Expected proportion of outliers (default 5%)
        """
        self.contamination = contamination
        self.model = IsolationForest(
            contamination=contamination,
            random_state=42,
            n_estimators=100
        )
        self.label_encoder = LabelEncoder()
    
    def detect_anomalies(self, df: pd.DataFrame) -> List[int]:
        """
        Detect anomalies in expense data
        
        Args:
            df: DataFrame with columns: id, amount, category, date
            
        Returns:
            List of expense IDs that are anomalies
        """
        if len(df) < 10:
            # Not enough data for anomaly detection
            return []
        
        # Prepare features
        features_df = df.copy()
        
        # Encode category
        features_df['category_encoded'] = self.label_encoder.fit_transform(features_df['category'])
        
        # Extract day of month if date column exists
        if 'date' in features_df.columns:
            features_df['day'] = pd.to_datetime(features_df['date']).dt.day
        else:
            features_df['day'] = 15  # Default mid-month
        
        # Select features for anomaly detection
        X = features_df[['amount', 'category_encoded']].values
        
        # Fit and predict
        predictions = self.model.fit_predict(X)
        
        # -1 indicates anomaly, 1 indicates normal
        anomaly_indices = np.where(predictions == -1)[0]
        anomaly_ids = df.iloc[anomaly_indices]['id'].tolist()
        
        return anomaly_ids
    
    def detect_category_anomalies(self, df: pd.DataFrame) -> List[int]:
        """
        Detect anomalies within each category separately
        More accurate for detecting unusual spending in specific categories
        
        Args:
            df: DataFrame with columns: id, amount, category
            
        Returns:
            List of expense IDs that are anomalies
        """
        if len(df) < 10:
            return []
        
        anomaly_ids = []
        
        for category in df['category'].unique():
            category_df = df[df['category'] == category].copy()
            
            # Need at least 5 records per category
            if len(category_df) < 5:
                continue
            
            # Calculate statistics
            amounts = category_df['amount'].values
            mean_amount = np.mean(amounts)
            std_amount = np.std(amounts)
            
            # Flag expenses > 2 standard deviations above mean
            threshold = mean_amount + (2 * std_amount)
            
            anomalies = category_df[category_df['amount'] > threshold]
            anomaly_ids.extend(anomalies['id'].tolist())
        
        return anomaly_ids
    
    def get_anomaly_score(self, df: pd.DataFrame) -> pd.Series:
        """
        Get anomaly scores for all expenses
        Lower scores indicate more anomalous behavior
        
        Args:
            df: DataFrame with expense data
            
        Returns:
            Series of anomaly scores indexed by expense ID
        """
        if len(df) < 10:
            return pd.Series(index=df['id'], data=0.0)
        
        features_df = df.copy()
        features_df['category_encoded'] = self.label_encoder.fit_transform(features_df['category'])
        
        X = features_df[['amount', 'category_encoded']].values
        
        # Fit model and get scores
        self.model.fit(X)
        scores = self.model.score_samples(X)
        
        return pd.Series(index=df['id'], data=scores)
