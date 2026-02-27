"""
Feature Engineering Pipeline for Telecom Churn Prediction
Phase 2: Feature Engineering with Business Logic
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split

class ChurnFeatureEngineer:
    """Feature engineering pipeline with business-driven features"""
    
    def __init__(self):
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.feature_names = []
        
    def load_data(self, filepath):
        """Load and perform initial cleaning"""
        df = pd.read_csv(filepath)
        
        # Handle TotalCharges - convert to numeric
        df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
        df['TotalCharges'].fillna(df['TotalCharges'].median(), inplace=True)
        
        # Convert target to binary
        df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})
        
        return df
    
    def create_business_features(self, df):
        """Create business-driven features"""
        df = df.copy()
        
        # 1. Tenure buckets - customer lifecycle stage
        df['tenure_bucket'] = pd.cut(df['tenure'], 
                                      bins=[0, 12, 36, 72],
                                      labels=['new', 'mid', 'loyal'])
        
        # 2. Monthly charge per service ratio
        service_cols = ['PhoneService', 'InternetService', 'OnlineSecurity', 
                       'OnlineBackup', 'DeviceProtection', 'TechSupport', 
                       'StreamingTV', 'StreamingMovies']
        
        df['total_services'] = 0
        for col in service_cols:
            if col in df.columns:
                df['total_services'] += (df[col] == 'Yes').astype(int)
        
        df['charge_per_service'] = df['MonthlyCharges'] / (df['total_services'] + 1)
        
        # 3. Customer value score
        df['customer_value'] = df['tenure'] * df['MonthlyCharges']
        
        # 4. Has premium services
        df['has_premium'] = ((df['OnlineSecurity'] == 'Yes') | 
                            (df['TechSupport'] == 'Yes')).astype(int)
        
        return df
    
    def encode_features(self, df, fit=True):
        """Encode categorical variables"""
        df = df.copy()
        
        # Binary encoding
        binary_cols = ['gender', 'Partner', 'Dependents', 'PhoneService', 
                      'PaperlessBilling']
        for col in binary_cols:
            if col in df.columns:
                df[col] = df[col].map({'Yes': 1, 'No': 0, 'Male': 1, 'Female': 0})
        
        # Multi-class encoding
        multi_cols = ['InternetService', 'Contract', 'PaymentMethod', 
                     'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
                     'TechSupport', 'StreamingTV', 'StreamingMovies', 
                     'MultipleLines', 'tenure_bucket']
        
        for col in multi_cols:
            if col in df.columns:
                if fit:
                    self.label_encoders[col] = LabelEncoder()
                    df[col] = self.label_encoders[col].fit_transform(df[col].astype(str))
                else:
                    df[col] = self.label_encoders[col].transform(df[col].astype(str))
        
        return df
    
    def prepare_features(self, df, target_col='Churn', fit=True):
        """Complete feature preparation pipeline"""
        # Drop customerID
        if 'customerID' in df.columns:
            df = df.drop('customerID', axis=1)
        
        # Separate features and target
        if target_col in df.columns:
            X = df.drop(target_col, axis=1)
            y = df[target_col]
        else:
            X = df
            y = None
        
        # Scale numerical features
        num_cols = ['tenure', 'MonthlyCharges', 'TotalCharges', 
                   'total_services', 'charge_per_service', 'customer_value']
        
        if fit:
            X[num_cols] = self.scaler.fit_transform(X[num_cols])
        else:
            X[num_cols] = self.scaler.transform(X[num_cols])
        
        self.feature_names = X.columns.tolist()
        
        return X, y

    
    def split_data(self, X, y, test_size=0.2, random_state=42):
        """Stratified train-test split"""
        return train_test_split(X, y, test_size=test_size, 
                               stratify=y, random_state=random_state)
    
    def get_feature_names(self):
        """Return feature names after transformation"""
        return self.feature_names


def prepare_data_pipeline(filepath, test_size=0.2):
    """Complete data preparation pipeline"""
    engineer = ChurnFeatureEngineer()
    
    # Load data
    df = engineer.load_data(filepath)
    print(f"✓ Data loaded: {df.shape}")
    
    # Create business features
    df = engineer.create_business_features(df)
    print(f"✓ Business features created")
    
    # Encode features
    df = engineer.encode_features(df, fit=True)
    print(f"✓ Features encoded")
    
    # Prepare features
    X, y = engineer.prepare_features(df, fit=True)
    print(f"✓ Features prepared: {X.shape}")
    
    # Split data
    X_train, X_test, y_train, y_test = engineer.split_data(X, y, test_size)
    print(f"✓ Data split - Train: {X_train.shape}, Test: {X_test.shape}")
    
    # Class distribution
    print(f"\nClass distribution:")
    print(f"  Train - Churn: {y_train.sum()}, No Churn: {len(y_train)-y_train.sum()}")
    print(f"  Test  - Churn: {y_test.sum()}, No Churn: {len(y_test)-y_test.sum()}")
    
    return X_train, X_test, y_train, y_test, engineer
