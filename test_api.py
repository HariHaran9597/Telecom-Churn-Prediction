"""
API Testing Script
Quick test of all API endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_root():
    """Test root endpoint"""
    print("Testing root endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print("✓ Root endpoint working\n")

def test_health():
    """Test health check"""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print("✓ Health check working\n")

def test_single_prediction():
    """Test single customer prediction"""
    print("Testing single prediction...")
    
    customer = {
        "gender": "Male",
        "SeniorCitizen": 0,
        "Partner": "Yes",
        "Dependents": "No",
        "tenure": 12,
        "PhoneService": "Yes",
        "MultipleLines": "No",
        "InternetService": "Fiber optic",
        "OnlineSecurity": "No",
        "OnlineBackup": "No",
        "DeviceProtection": "No",
        "TechSupport": "No",
        "StreamingTV": "Yes",
        "StreamingMovies": "Yes",
        "Contract": "Month-to-month",
        "PaperlessBilling": "Yes",
        "PaymentMethod": "Electronic check",
        "MonthlyCharges": 85.0,
        "TotalCharges": 1020.0
    }
    
    response = requests.post(f"{BASE_URL}/predict", json=customer)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Churn Probability: {result['churn_probability']:.2%}")
        print(f"Risk Score: {result['risk_score']}/100")
        print(f"Risk Tier: {result['risk_tier']}")
        print(f"Customer Value: ₹{result['customer_value']:,.0f}")
        print(f"Recommended Action: {result['recommended_action']}")
        print("✓ Single prediction working\n")
    else:
        print(f"✗ Error: {response.text}\n")

def test_bulk_prediction():
    """Test bulk prediction with CSV"""
    print("Testing bulk prediction...")
    
    try:
        with open('data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv', 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{BASE_URL}/predict/bulk", files=files)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Total Customers: {result['total_customers']}")
            print(f"High Risk: {result['high_risk_customers']}")
            print(f"Revenue at Risk: {result['total_revenue_at_risk']}")
            print(f"Intervention Plan:")
            for key, value in result['intervention_plan'].items():
                print(f"  {key}: {value}")
            print("✓ Bulk prediction working\n")
        else:
            print(f"✗ Error: {response.text}\n")
    except FileNotFoundError:
        print("⚠ Dataset not found. Run download_data.py first\n")

if __name__ == "__main__":
    print("="*60)
    print("API TESTING SUITE")
    print("="*60)
    print("\nMake sure API is running: uvicorn src.api:app --reload\n")
    
    try:
        test_root()
        test_health()
        test_single_prediction()
        test_bulk_prediction()
        
        print("="*60)
        print("ALL TESTS COMPLETED")
        print("="*60)
    except requests.exceptions.ConnectionError:
        print("✗ Error: Cannot connect to API")
        print("Start the API first: uvicorn src.api:app --reload")
