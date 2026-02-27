"""
Model Training with MLflow Tracking
Phase 3: MLOps with Experiment Tracking
"""
import mlflow
import mlflow.sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                            f1_score, roc_auc_score, confusion_matrix)
from imblearn.over_sampling import SMOTE
import numpy as np
import joblib
import os

class ChurnModelTrainer:
    """Train and evaluate churn prediction models with MLflow"""
    
    def __init__(self, experiment_name="telecom-churn-prediction"):
        mlflow.set_experiment(experiment_name)
        self.best_model = None
        self.best_score = 0
        
    def evaluate_model(self, model, X_test, y_test):
        """Calculate all evaluation metrics"""
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1]
        
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred),
            'recall': recall_score(y_test, y_pred),
            'f1_score': f1_score(y_test, y_pred),
            'roc_auc': roc_auc_score(y_test, y_pred_proba)
        }
        
        return metrics, y_pred, y_pred_proba

    
    def train_with_mlflow(self, model, model_name, params, X_train, y_train, 
                         X_test, y_test, use_smote=False):
        """Train model and log to MLflow"""
        
        with mlflow.start_run(run_name=model_name):
            # Apply SMOTE if requested
            if use_smote:
                smote = SMOTE(random_state=42)
                X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)
                mlflow.log_param("resampling", "SMOTE")
            else:
                X_train_resampled, y_train_resampled = X_train, y_train
                mlflow.log_param("resampling", "None")
            
            # Log parameters
            for param, value in params.items():
                mlflow.log_param(param, value)
            
            # Train model
            model.fit(X_train_resampled, y_train_resampled)
            
            # Evaluate
            metrics, y_pred, y_pred_proba = self.evaluate_model(model, X_test, y_test)
            
            # Log metrics
            for metric_name, metric_value in metrics.items():
                mlflow.log_metric(metric_name, metric_value)
            
            # Log model
            mlflow.sklearn.log_model(model, "model")
            
            # Track best model
            if metrics['roc_auc'] > self.best_score:
                self.best_score = metrics['roc_auc']
                self.best_model = model
                
                # Save best model locally
                os.makedirs('models', exist_ok=True)
                joblib.dump(model, 'models/best_model.pkl')
                mlflow.log_artifact('models/best_model.pkl')
            
            print(f"\n{model_name} Results:")
            for metric, value in metrics.items():
                print(f"  {metric}: {value:.4f}")
            
            return metrics

    
    def run_all_experiments(self, X_train, y_train, X_test, y_test):
        """Run all model experiments"""
        
        print("="*60)
        print("Starting MLflow Experiments")
        print("="*60)
        
        results = {}
        
        # 1. Logistic Regression
        lr_params = {'C': 1.0, 'max_iter': 1000, 'solver': 'lbfgs'}
        lr_model = LogisticRegression(**lr_params, random_state=42)
        results['Logistic Regression'] = self.train_with_mlflow(
            lr_model, "Logistic Regression", lr_params, 
            X_train, y_train, X_test, y_test
        )
        
        # 2. Decision Tree
        dt_params = {'max_depth': 10, 'min_samples_split': 20, 'min_samples_leaf': 10}
        dt_model = DecisionTreeClassifier(**dt_params, random_state=42)
        results['Decision Tree'] = self.train_with_mlflow(
            dt_model, "Decision Tree", dt_params,
            X_train, y_train, X_test, y_test
        )
        
        # 3. Random Forest
        rf_params = {'n_estimators': 100, 'max_depth': 15, 'min_samples_split': 10}
        rf_model = RandomForestClassifier(**rf_params, random_state=42)
        results['Random Forest'] = self.train_with_mlflow(
            rf_model, "Random Forest", rf_params,
            X_train, y_train, X_test, y_test
        )
        
        # 4. XGBoost
        xgb_params = {'n_estimators': 100, 'max_depth': 6, 'learning_rate': 0.1, 
                     'scale_pos_weight': 3}
        xgb_model = XGBClassifier(**xgb_params, random_state=42, eval_metric='logloss')
        results['XGBoost'] = self.train_with_mlflow(
            xgb_model, "XGBoost", xgb_params,
            X_train, y_train, X_test, y_test
        )
        
        # 5. XGBoost with SMOTE
        results['XGBoost + SMOTE'] = self.train_with_mlflow(
            XGBClassifier(**xgb_params, random_state=42, eval_metric='logloss'),
            "XGBoost + SMOTE", xgb_params,
            X_train, y_train, X_test, y_test, use_smote=True
        )
        
        print("\n" + "="*60)
        print("All Experiments Completed!")
        print(f"Best Model AUC: {self.best_score:.4f}")
        print("="*60)
        
        return results


if __name__ == "__main__":
    from features import prepare_data_pipeline
    
    # Prepare data
    X_train, X_test, y_train, y_test, engineer = prepare_data_pipeline(
        'data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv'
    )
    
    # Train models
    trainer = ChurnModelTrainer()
    results = trainer.run_all_experiments(X_train, y_train, X_test, y_test)
    
    print("\n✓ Training complete! View results in MLflow UI:")
    print("  Run: mlflow ui")
    print("  Then open: http://localhost:5000")
