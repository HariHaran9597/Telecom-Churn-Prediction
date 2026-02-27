"""
Complete Training Pipeline
Trains model and saves all artifacts
"""
import sys
sys.path.append('src')
from features import prepare_data_pipeline, ChurnFeatureEngineer
from model import ChurnModelTrainer
import joblib
import os

def main():
    print("="*60)
    print("TELECOM CHURN PREDICTION - TRAINING PIPELINE")
    print("="*60)
    
    # Step 1: Prepare data
    print("\n[1/3] Preparing data...")
    X_train, X_test, y_train, y_test, engineer = prepare_data_pipeline(
        'data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv'
    )
    
    # Save feature engineer
    os.makedirs('models', exist_ok=True)
    joblib.dump(engineer, 'models/feature_engineer.pkl')
    print("✓ Feature engineer saved")
    
    # Step 2: Train models with MLflow
    print("\n[2/3] Training models with MLflow...")
    trainer = ChurnModelTrainer()
    results = trainer.run_all_experiments(X_train, y_train, X_test, y_test)
    
    # Step 3: Summary
    print("\n[3/3] Training Summary")
    print("="*60)
    print("\nModel Performance (AUC):")
    for model_name, metrics in results.items():
        print(f"  {model_name:20s}: {metrics['roc_auc']:.4f}")
    
    print(f"\n✓ Best model saved to: models/best_model.pkl")
    print(f"✓ Feature engineer saved to: models/feature_engineer.pkl")
    print("\n" + "="*60)
    print("NEXT STEPS:")
    print("="*60)
    print("1. View MLflow UI:")
    print("   mlflow ui")
    print("   Open: http://localhost:5000")
    print("\n2. Start API server:")
    print("   uvicorn src.api:app --reload")
    print("\n3. Launch Streamlit dashboard:")
    print("   streamlit run app.py")
    print("="*60)

if __name__ == "__main__":
    main()
