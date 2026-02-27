# 📊 Telecom Churn Prediction with MLOps Pipeline and Business Impact Dashboard

> An end-to-end MLOps project that goes beyond accuracy metrics to deliver real business value through revenue impact analysis and actionable retention strategies.

[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/)
[![MLflow](https://img.shields.io/badge/MLflow-Tracking-orange.svg)](https://mlflow.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-API-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red.svg)](https://streamlit.io/)

## 🎯 What Makes This Project Different?

Most churn prediction projects stop at model accuracy. This project delivers what consulting firms like Mu Sigma and Fractal present to clients:

**"If we act on the top 500 high-risk customers this month, we retain ₹X revenue with Y% ROI"**

### Key Differentiators
- ✅ **MLflow Integration**: Complete experiment tracking (95% of candidates skip this)
- ✅ **Business Impact Dashboard**: Translates predictions into rupee value
- ✅ **ROI Calculator**: Cost-benefit analysis for retention campaigns
- ✅ **Risk Segmentation**: Critical/Medium/Low risk tiers with action plans
- ✅ **Production Ready**: FastAPI backend + Streamlit frontend + Render deployment

## 🚀 Quick Start (5 minutes)

```bash
# 1. Setup environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Download dataset
python download_data.py

# 3. Train models with MLflow
python train_pipeline.py

# 4. Launch modern dashboard
streamlit run app.py
```

**New!** 🎨 Modern dark theme UI with professional styling and enhanced visualizations!

See [QUICKSTART.md](QUICKSTART.md) for detailed instructions.

## 📁 Project Structure

```
telecom-churn-mlops/
├── data/
│   ├── raw/                           # IBM Telco dataset
│   └── processed/                     # Engineered features
├── notebooks/
│   └── 01_eda_business_insights.ipynb # Business-focused EDA
├── src/
│   ├── features.py                    # Feature engineering pipeline
│   ├── model.py                       # MLflow experiment tracking
│   ├── business.py                    # Business impact calculator
│   └── api.py                         # FastAPI backend
├── models/                            # Saved models & artifacts
├── mlruns/                            # MLflow tracking data
├── app.py                             # Streamlit dashboard
├── train_pipeline.py                  # Complete training script
└── requirements.txt
```

## 🔬 Technical Implementation

### Phase 1: Business-Driven EDA
- Churn analysis by contract type, tenure, and services
- Every insight translated to business recommendation
- Focus on actionable patterns, not just statistics

### Phase 2: Feature Engineering
```python
# Business-driven features
- tenure_bucket: Customer lifecycle stage (new/mid/loyal)
- charge_per_service: Value per service ratio
- total_services: Service adoption count
- customer_value: Lifetime value estimation
- has_premium: Premium service indicator
```

### Phase 3: MLflow Experiment Tracking
5 models trained and logged:
1. Logistic Regression (baseline)
2. Decision Tree
3. Random Forest
4. XGBoost
5. XGBoost + SMOTE (class imbalance handling)

All experiments tracked with:
- Parameters (hyperparameters, resampling method)
- Metrics (accuracy, precision, recall, F1, AUC)
- Model artifacts (serialized models)

### Phase 4: Business Impact Layer
```python
# Key business metrics
- Revenue at Risk: Total annual revenue from high-risk customers
- Risk Score: 0-100 scale for easy interpretation
- Risk Tiers: Critical (>70%), Medium (40-70%), Low (<40%)
- ROI Analysis: Intervention cost vs expected revenue saved
```

### Phase 5: Deployment

**Streamlit Dashboard:**
- Single customer prediction with risk gauge
- Bulk CSV analysis with business impact summary
- Interactive visualizations (Plotly)
- Downloadable results

**FastAPI Backend:**
- `/predict` - Single customer endpoint
- `/predict/bulk` - Batch processing
- `/health` - Service health check
- Auto-generated API docs at `/docs`

## 📊 Business Impact Metrics

### Example Output
```
Total Customers: 7,043
High Risk Customers: 1,521
Revenue at Risk: ₹12,84,000

Intervention Plan (Top 500):
├─ Customers Targeted: 500
├─ Intervention Cost: ₹5,000
├─ Expected Revenue Saved: ₹1,26,000
├─ Net Benefit: ₹1,21,000
└─ ROI: 2,420%
```

## 🎓 Learning Outcomes

This project demonstrates:
- ✅ End-to-end ML pipeline development
- ✅ MLOps best practices (experiment tracking, versioning)
- ✅ Business value translation (not just technical metrics)
- ✅ Production deployment (API + Dashboard)
- ✅ Consulting-style thinking (ROI, cost-benefit analysis)

## 🛠️ Tech Stack

| Category | Technology |
|----------|-----------|
| ML/Data | pandas, numpy, scikit-learn, xgboost, imbalanced-learn |
| MLOps | MLflow |
| Backend | FastAPI, uvicorn |
| Frontend | Streamlit, Plotly |
| Deployment | Render |

## 📈 Model Performance

View detailed metrics in MLflow UI:
```bash
mlflow ui
# Open http://localhost:5000
```

Best model typically achieves:
- AUC: ~0.84-0.86
- Precision: ~0.65-0.70
- Recall: ~0.75-0.80
- F1 Score: ~0.70-0.75

## 🚢 Deployment

### Local Development
```bash
# API Server
uvicorn src.api:app --reload

# Streamlit Dashboard
streamlit run app.py
```

### Production (Render)
1. Push to GitHub
2. Connect repository to Render
3. Deploy using `render.yaml` configuration
4. Environment auto-configured

## 📝 Usage Examples

### Single Customer Prediction
```python
import requests

customer = {
    "gender": "Male",
    "tenure": 12,
    "MonthlyCharges": 70.0,
    "Contract": "Month-to-month",
    # ... other features
}

response = requests.post("http://localhost:8000/predict", json=customer)
print(response.json())
# {
#   "churn_probability": 0.73,
#   "risk_score": 73,
#   "risk_tier": "Critical Risk",
#   "recommended_action": "Immediate personal outreach + premium retention offer"
# }
```

### Bulk Analysis
```python
files = {'file': open('customers.csv', 'rb')}
response = requests.post("http://localhost:8000/predict/bulk", files=files)
print(response.json()['intervention_plan'])
```

## 🤝 Contributing

This is a portfolio project, but suggestions are welcome! Open an issue or submit a PR.

## 📄 License

MIT License - feel free to use this project for learning and portfolio purposes.

## 🙏 Acknowledgments

- Dataset: IBM Telco Customer Churn
- Inspired by real-world consulting projects at Mu Sigma and Fractal Analytics

---

**Built with focus on production-ready MLOps practices and business value delivery.**

*For detailed setup instructions, see [QUICKSTART.md](QUICKSTART.md)*
