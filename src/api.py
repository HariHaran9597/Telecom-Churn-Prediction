"""
FastAPI Backend for Churn Prediction
Phase 5: Deployment API
"""
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib
import numpy as np
from typing import List, Dict
import io
import sys
import os

# Add src directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from business import BusinessImpactCalculator

app = FastAPI(title="Telecom Churn Prediction API",
             description="Predict customer churn with business impact analysis",
             version="1.0.0")

# Load model and feature engineer
try:
    model = joblib.load('models/best_model.pkl')
    engineer = joblib.load('models/feature_engineer.pkl')
    print("✓ Model and feature engineer loaded")
except:
    model = None
    engineer = None
    print("⚠ Model not found. Train model first using src/model.py")

# Initialize business calculator
business_calc = BusinessImpactCalculator()

class CustomerInput(BaseModel):
    """Single customer input schema"""
    gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float


class PredictionResponse(BaseModel):
    """Prediction response schema"""
    churn_probability: float
    risk_score: int
    risk_tier: str
    recommended_action: str
    customer_value: float

@app.get("/")
def root():
    """API health check"""
    return {
        "message": "Telecom Churn Prediction API",
        "status": "active",
        "model_loaded": model is not None
    }

@app.post("/predict", response_model=PredictionResponse)
def predict_single(customer: CustomerInput):
    """Predict churn for a single customer"""
    
    if model is None or engineer is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Convert to DataFrame
        customer_dict = customer.dict()
        df = pd.DataFrame([customer_dict])
        
        # Feature engineering
        df = engineer.create_business_features(df)
        df = engineer.encode_features(df, fit=False)
        X, _ = engineer.prepare_features(df, target_col=None, fit=False)
        
        # Predict
        churn_prob = model.predict_proba(X)[0][1]
        
        # Business metrics
        risk_score = business_calc.calculate_risk_score(churn_prob)
        risk_tier = business_calc.assign_risk_tier(churn_prob)
        customer_value = business_calc.calculate_customer_lifetime_value(
            customer.MonthlyCharges, customer.tenure
        )
        recommended_action = business_calc.recommend_action(churn_prob, customer_value)
        
        return PredictionResponse(
            churn_probability=float(churn_prob),
            risk_score=risk_score,
            risk_tier=risk_tier,
            recommended_action=recommended_action,
            customer_value=float(customer_value)
        )
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")


@app.post("/predict/bulk")
def predict_bulk(file: UploadFile = File(...)):
    """Predict churn for multiple customers from CSV"""
    
    if model is None or engineer is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Read CSV
        contents = file.file.read()
        df = pd.read_csv(io.BytesIO(contents))
        
        # Store original data
        df_original = df.copy()
        
        # Feature engineering
        df = engineer.create_business_features(df)
        df = engineer.encode_features(df, fit=False)
        X, _ = engineer.prepare_features(df, target_col=None, fit=False)
        
        # Predict
        churn_probs = model.predict_proba(X)[:, 1]
        
        # Add predictions to original data
        df_original['churn_probability'] = churn_probs
        
        # Generate business report
        report, df_segmented = business_calc.generate_business_report(df_original)
        
        return {
            "total_customers": report['total_customers'],
            "high_risk_customers": report['high_risk_customers'],
            "medium_risk_customers": report['medium_risk_customers'],
            "total_revenue_at_risk": f"₹{report['total_revenue_at_risk']:,.2f}",
            "intervention_plan": {
                "customers_targeted": report['intervention_plan']['customers_targeted'],
                "intervention_cost": f"₹{report['intervention_plan']['intervention_cost']:,.2f}",
                "expected_revenue_saved": f"₹{report['intervention_plan']['expected_revenue_saved']:,.2f}",
                "net_benefit": f"₹{report['intervention_plan']['net_benefit']:,.2f}",
                "roi_percentage": f"{report['intervention_plan']['roi_percentage']:.1f}%"
            },
            "predictions": df_segmented[['churn_probability', 'risk_score', 'risk_tier']].to_dict('records')[:10]
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bulk prediction error: {str(e)}")

@app.get("/health")
def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "engineer_loaded": engineer is not None
    }
