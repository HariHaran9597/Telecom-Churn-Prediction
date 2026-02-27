"""
Streamlit Dashboard for Churn Prediction
Phase 5: Modern Yellow & Black Theme
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import joblib
import sys
sys.path.append('src')
from business import BusinessImpactCalculator

# Page config
st.set_page_config(
    page_title="Telecom Churn Prediction",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Yellow & Black theme
st.markdown("""
<style>
    /* Main background - Pure Black */
    .stApp {
        background-color: #000000;
    }
    
    /* Sidebar - Dark with yellow accent */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #000000 0%, #1a1a1a 100%);
        border-right: 2px solid #FFD700;
    }
    
    /* Headers - Yellow */
    h1, h2, h3 {
        color: #FFD700 !important;
        font-weight: 700;
        text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #FFD700 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #FFD700 !important;
        font-weight: 500;
        opacity: 0.8;
    }
    
    /* Buttons - Yellow with black text */
    .stButton>button {
        background-color: #FFD700;
        color: #000000;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 700;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #FFC700;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 215, 0, 0.6);
    }
    
    /* Input fields */
    .stSelectbox label, .stNumberInput label, .stSlider label {
        color: #FFD700 !important;
        font-weight: 500;
    }
    
    .stSelectbox > div > div, .stNumberInput > div > div {
        background-color: #1a1a1a;
        border: 1px solid #FFD700;
        color: #FFD700;
    }
    
    /* Text color */
    p, span, div {
        color: #FFD700;
    }
    
    /* Success/Info boxes */
    .stSuccess {
        background-color: #1a1a1a;
        border-left: 4px solid #FFD700;
        color: #FFD700;
    }
    
    .stInfo {
        background-color: #1a1a1a;
        border-left: 4px solid #FFD700;
        color: #FFD700;
    }
    
    .stError {
        background-color: #1a1a1a;
        border-left: 4px solid #FFD700;
        color: #FFD700;
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background-color: #1a1a1a;
        border: 2px dashed #FFD700;
        border-radius: 10px;
    }
    
    [data-testid="stFileUploader"] label {
        color: #FFD700 !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #1a1a1a;
        border: 1px solid #FFD700;
        color: #FFD700 !important;
        font-weight: 600;
    }
    
    /* Dataframe */
    .dataframe {
        color: #FFD700 !important;
    }
    
    /* Markdown */
    .stMarkdown {
        color: #FFD700;
    }
    
    /* Divider */
    hr {
        border-color: #FFD700;
        opacity: 0.3;
    }
    
    /* Radio buttons */
    .stRadio label {
        color: #FFD700 !important;
    }
    
    /* Download button */
    .stDownloadButton>button {
        background-color: #FFD700;
        color: #000000;
        border: none;
        font-weight: 700;
    }
    
    .stDownloadButton>button:hover {
        background-color: #FFC700;
    }
</style>
""", unsafe_allow_html=True)

# Load model
@st.cache_resource
def load_model():
    try:
        model = joblib.load('models/best_model.pkl')
        engineer = joblib.load('models/feature_engineer.pkl')
        return model, engineer
    except:
        return None, None

model, engineer = load_model()
business_calc = BusinessImpactCalculator()

# Header with yellow and black theme
st.markdown("""
    <div style='text-align: center; padding: 2rem 0; background-color: #000000;'>
        <h1 style='font-size: 3.5rem; margin-bottom: 0.5rem; color: #FFD700;'>
            ⚡ TELECOM CHURN PREDICTION
        </h1>
        <p style='color: #FFD700; font-size: 1.3rem; opacity: 0.9;'>
            AI-Powered Customer Retention & Business Impact Analysis
        </p>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# Sidebar
st.sidebar.markdown("""
    <div style='text-align: center; padding: 1rem 0; background-color: #000000;'>
        <h2 style='color: #FFD700; margin-bottom: 0; font-size: 1.8rem;'>⚡ NAVIGATION</h2>
    </div>
""", unsafe_allow_html=True)

mode = st.sidebar.radio(
    "Select Mode",
    ["🔍 Single Customer Prediction", "📊 Bulk Analysis & ROI"],
    label_visibility="collapsed"
)

# Sidebar info
st.sidebar.markdown("---")
st.sidebar.markdown("""
    <div style='padding: 1.5rem; background-color: #1a1a1a; border: 2px solid #FFD700; border-radius: 10px; margin-top: 1rem;'>
        <h3 style='color: #FFD700; font-size: 1.1rem; margin-bottom: 0.5rem;'>💡 ABOUT</h3>
        <p style='color: #FFD700; font-size: 0.95rem; margin: 0; opacity: 0.9;'>
            This AI system predicts customer churn and calculates business impact with ROI analysis.
        </p>
    </div>
""", unsafe_allow_html=True)

if model is None:
    st.error("⚠️ Model not loaded. Please train the model first using `python train_pipeline.py`")
    st.stop()


# Mode 1: Single Customer Prediction
if mode == "🔍 Single Customer Prediction":
    st.markdown("""
        <div style='background-color: #1a1a1a; padding: 1.5rem; border: 2px solid #FFD700; border-radius: 10px; margin-bottom: 2rem;'>
            <h2 style='color: #FFD700; margin: 0; font-size: 1.8rem;'>🔍 SINGLE CUSTOMER CHURN PREDICTION</h2>
            <p style='color: #FFD700; margin-top: 0.5rem; opacity: 0.8;'>Enter customer details to get instant risk assessment</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 👤 DEMOGRAPHICS")
        gender = st.selectbox("Gender", ["Male", "Female"])
        senior_citizen = st.selectbox("Senior Citizen", [0, 1])
        partner = st.selectbox("Partner", ["Yes", "No"])
        dependents = st.selectbox("Dependents", ["Yes", "No"])
        tenure = st.slider("Tenure (months)", 0, 72, 12)
    
    with col2:
        st.markdown("### 📱 SERVICES")
        phone_service = st.selectbox("Phone Service", ["Yes", "No"])
        multiple_lines = st.selectbox("Multiple Lines", ["Yes", "No", "No phone service"])
        internet_service = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
        online_security = st.selectbox("Online Security", ["Yes", "No", "No internet service"])
        online_backup = st.selectbox("Online Backup", ["Yes", "No", "No internet service"])
        device_protection = st.selectbox("Device Protection", ["Yes", "No", "No internet service"])
        tech_support = st.selectbox("Tech Support", ["Yes", "No", "No internet service"])
        streaming_tv = st.selectbox("Streaming TV", ["Yes", "No", "No internet service"])
        streaming_movies = st.selectbox("Streaming Movies", ["Yes", "No", "No internet service"])
    
    with col3:
        st.markdown("### 💳 ACCOUNT INFO")
        contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
        paperless_billing = st.selectbox("Paperless Billing", ["Yes", "No"])
        payment_method = st.selectbox("Payment Method", 
            ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"])
        monthly_charges = st.number_input("Monthly Charges (₹)", 0.0, 200.0, 70.0)
        total_charges = st.number_input("Total Charges (₹)", 0.0, 10000.0, 840.0)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        predict_button = st.button("⚡ PREDICT CHURN RISK", type="primary", use_container_width=True)
    
    if predict_button:
        # Create input dataframe
        input_data = {
            'gender': gender, 'SeniorCitizen': senior_citizen, 'Partner': partner,
            'Dependents': dependents, 'tenure': tenure, 'PhoneService': phone_service,
            'MultipleLines': multiple_lines, 'InternetService': internet_service,
            'OnlineSecurity': online_security, 'OnlineBackup': online_backup,
            'DeviceProtection': device_protection, 'TechSupport': tech_support,
            'StreamingTV': streaming_tv, 'StreamingMovies': streaming_movies,
            'Contract': contract, 'PaperlessBilling': paperless_billing,
            'PaymentMethod': payment_method, 'MonthlyCharges': monthly_charges,
            'TotalCharges': total_charges
        }
        
        df = pd.DataFrame([input_data])
        
        # Feature engineering
        df = engineer.create_business_features(df)
        df = engineer.encode_features(df, fit=False)
        X, _ = engineer.prepare_features(df, target_col=None, fit=False)
        
        # Predict
        churn_prob = model.predict_proba(X)[0][1]
        risk_score = business_calc.calculate_risk_score(churn_prob)
        risk_tier = business_calc.assign_risk_tier(churn_prob)
        customer_value = business_calc.calculate_customer_lifetime_value(monthly_charges, tenure)
        action = business_calc.recommend_action(churn_prob, customer_value)
        
        # Display results
        st.markdown("---")
        st.markdown("""
            <div style='text-align: center; padding: 1rem; background-color: #000000;'>
                <h2 style='color: #FFD700; font-size: 2rem;'>📈 PREDICTION RESULTS</h2>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
                <div style='background-color: #1a1a1a; border: 2px solid #FFD700; padding: 1.5rem; border-radius: 10px; text-align: center;'>
                    <p style='color: #FFD700; margin: 0; font-size: 0.9rem; opacity: 0.8;'>CHURN PROBABILITY</p>
                    <h2 style='color: #FFD700; margin: 0.5rem 0; font-size: 2.5rem;'>{churn_prob*100:.1f}%</h2>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div style='background-color: #1a1a1a; border: 2px solid #FFD700; padding: 1.5rem; border-radius: 10px; text-align: center;'>
                    <p style='color: #FFD700; margin: 0; font-size: 0.9rem; opacity: 0.8;'>RISK SCORE</p>
                    <h2 style='color: #FFD700; margin: 0.5rem 0; font-size: 2.5rem;'>{risk_score}/100</h2>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div style='background-color: #1a1a1a; border: 2px solid #FFD700; padding: 1.5rem; border-radius: 10px; text-align: center;'>
                    <p style='color: #FFD700; margin: 0; font-size: 0.9rem; opacity: 0.8;'>RISK TIER</p>
                    <h2 style='color: #FFD700; margin: 0.5rem 0; font-size: 1.5rem;'>{risk_tier}</h2>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
                <div style='background-color: #1a1a1a; border: 2px solid #FFD700; padding: 1.5rem; border-radius: 10px; text-align: center;'>
                    <p style='color: #FFD700; margin: 0; font-size: 0.9rem; opacity: 0.8;'>CUSTOMER VALUE</p>
                    <h2 style='color: #FFD700; margin: 0.5rem 0; font-size: 2rem;'>₹{customer_value:,.0f}</h2>
                </div>
            """, unsafe_allow_html=True)
        
        # Risk gauge with yellow and black
        st.markdown("<br>", unsafe_allow_html=True)
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=churn_prob*100,
            title={'text': "CHURN RISK LEVEL", 'font': {'size': 24, 'color': '#FFD700'}},
            number={'font': {'color': '#FFD700', 'size': 48}},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 2, 'tickcolor': "#FFD700", 'tickfont': {'color': '#FFD700'}},
                'bar': {'color': "#FFD700", 'thickness': 0.75},
                'bgcolor': "#000000",
                'borderwidth': 3,
                'bordercolor': "#FFD700",
                'steps': [
                    {'range': [0, 40], 'color': "#1a1a1a"},
                    {'range': [40, 70], 'color': "#2a2a2a"},
                    {'range': [70, 100], 'color': "#3a3a3a"}
                ],
                'threshold': {
                    'line': {'color': "#FFD700", 'width': 4},
                    'thickness': 0.75,
                    'value': 70
                }
            }
        ))
        
        fig.update_layout(
            paper_bgcolor="#000000",
            plot_bgcolor="#000000",
            font={'color': "#FFD700", 'family': "Arial"},
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Recommendation
        st.markdown(f"""
            <div style='background-color: #1a1a1a; border: 2px solid #FFD700; border-left: 5px solid #FFD700;
                        padding: 2rem; border-radius: 10px; margin-top: 2rem;'>
                <h3 style='color: #FFD700; margin-top: 0; font-size: 1.3rem;'>💡 RECOMMENDED ACTION</h3>
                <p style='color: #FFD700; font-size: 1.1rem; margin-bottom: 0; opacity: 0.9;'>{action}</p>
            </div>
        """, unsafe_allow_html=True)


# Mode 2: Bulk Analysis
else:
    st.markdown("""
        <div style='background-color: #1a1a1a; padding: 1.5rem; border: 2px solid #FFD700; border-radius: 10px; margin-bottom: 2rem;'>
            <h2 style='color: #FFD700; margin: 0; font-size: 1.8rem;'>📊 BULK CUSTOMER ANALYSIS & BUSINESS IMPACT</h2>
            <p style='color: #FFD700; margin-top: 0.5rem; opacity: 0.8;'>Upload CSV file for comprehensive ROI analysis</p>
        </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("📁 Upload Customer Data (CSV)", type=['csv'])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success(f"✓ Loaded {len(df):,} customers")
        
        # Show sample
        with st.expander("👁️ View Sample Data"):
            st.dataframe(df.head(), use_container_width=True)
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            analyze_button = st.button("⚡ RUN ANALYSIS", type="primary", use_container_width=True)
        
        if analyze_button:
            with st.spinner("🔄 Analyzing customers..."):
                # Store original
                df_original = df.copy()
                
                # Feature engineering
                df = engineer.create_business_features(df)
                df = engineer.encode_features(df, fit=False)
                X, _ = engineer.prepare_features(df, target_col=None, fit=False)
                
                # Predict
                churn_probs = model.predict_proba(X)[:, 1]
                df_original['churn_probability'] = churn_probs
                
                # Business report
                report, df_segmented = business_calc.generate_business_report(df_original, top_n=500)
                
                # Display metrics
                st.markdown("---")
                st.markdown("""
                    <div style='text-align: center; padding: 1rem; background-color: #000000;'>
                        <h2 style='color: #FFD700; font-size: 2rem;'>📊 BUSINESS IMPACT SUMMARY</h2>
                    </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown(f"""
                        <div style='background-color: #1a1a1a; border: 2px solid #FFD700; padding: 1.5rem; border-radius: 10px; text-align: center;'>
                            <p style='color: #FFD700; margin: 0; font-size: 0.9rem; opacity: 0.8;'>TOTAL CUSTOMERS</p>
                            <h2 style='color: #FFD700; margin: 0.5rem 0; font-size: 2.5rem;'>{report['total_customers']:,}</h2>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                        <div style='background-color: #1a1a1a; border: 2px solid #FFD700; padding: 1.5rem; border-radius: 10px; text-align: center;'>
                            <p style='color: #FFD700; margin: 0; font-size: 0.9rem; opacity: 0.8;'>HIGH RISK</p>
                            <h2 style='color: #FFD700; margin: 0.5rem 0; font-size: 2.5rem;'>{report['high_risk_customers']:,}</h2>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                        <div style='background-color: #1a1a1a; border: 2px solid #FFD700; padding: 1.5rem; border-radius: 10px; text-align: center;'>
                            <p style='color: #FFD700; margin: 0; font-size: 0.9rem; opacity: 0.8;'>MEDIUM RISK</p>
                            <h2 style='color: #FFD700; margin: 0.5rem 0; font-size: 2.5rem;'>{report['medium_risk_customers']:,}</h2>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    st.markdown(f"""
                        <div style='background-color: #1a1a1a; border: 2px solid #FFD700; padding: 1.5rem; border-radius: 10px; text-align: center;'>
                            <p style='color: #FFD700; margin: 0; font-size: 0.9rem; opacity: 0.8;'>REVENUE AT RISK</p>
                            <h2 style='color: #FFD700; margin: 0.5rem 0; font-size: 1.8rem;'>₹{report['total_revenue_at_risk']:,.0f}</h2>
                        </div>
                    """, unsafe_allow_html=True)
                
                # Intervention ROI
                st.markdown("---")
                st.markdown("""
                    <div style='text-align: center; padding: 1rem; background-color: #000000;'>
                        <h2 style='color: #FFD700; font-size: 2rem;'>💰 INTERVENTION ROI ANALYSIS (TOP 500)</h2>
                    </div>
                """, unsafe_allow_html=True)
                
                roi = report['intervention_plan']
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown(f"""
                        <div style='background-color: #1a1a1a; border: 2px solid #FFD700; padding: 1.5rem; border-radius: 10px; text-align: center;'>
                            <p style='color: #FFD700; margin: 0; font-size: 0.9rem; opacity: 0.8;'>CUSTOMERS TARGETED</p>
                            <h2 style='color: #FFD700; margin: 0.5rem 0; font-size: 2.5rem;'>{roi['customers_targeted']:,}</h2>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                        <div style='background-color: #1a1a1a; border: 2px solid #FFD700; padding: 1.5rem; border-radius: 10px; text-align: center;'>
                            <p style='color: #FFD700; margin: 0; font-size: 0.9rem; opacity: 0.8;'>INTERVENTION COST</p>
                            <h2 style='color: #FFD700; margin: 0.5rem 0; font-size: 1.8rem;'>₹{roi['intervention_cost']:,.0f}</h2>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                        <div style='background-color: #1a1a1a; border: 2px solid #FFD700; padding: 1.5rem; border-radius: 10px; text-align: center;'>
                            <p style='color: #FFD700; margin: 0; font-size: 0.9rem; opacity: 0.8;'>EXPECTED REVENUE SAVED</p>
                            <h2 style='color: #FFD700; margin: 0.5rem 0; font-size: 1.8rem;'>₹{roi['expected_revenue_saved']:,.0f}</h2>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    st.markdown(f"""
                        <div style='background-color: #1a1a1a; border: 2px solid #FFD700; padding: 1.5rem; border-radius: 10px; text-align: center;'>
                            <p style='color: #FFD700; margin: 0; font-size: 0.9rem; opacity: 0.8;'>NET BENEFIT</p>
                            <h2 style='color: #FFD700; margin: 0.5rem 0; font-size: 1.8rem;'>₹{roi['net_benefit']:,.0f}</h2>
                            <p style='color: #FFD700; margin: 0; font-size: 1rem; font-weight: 700;'>ROI: {roi['roi_percentage']:.1f}%</p>
                        </div>
                    """, unsafe_allow_html=True)
                
                # Risk distribution with yellow and black
                st.markdown("---")
                st.markdown("""
                    <div style='text-align: center; padding: 1rem; background-color: #000000;'>
                        <h2 style='color: #FFD700; font-size: 2rem;'>📈 RISK DISTRIBUTION</h2>
                    </div>
                """, unsafe_allow_html=True)
                
                risk_counts = df_segmented['risk_tier'].value_counts()
                fig = px.pie(
                    values=risk_counts.values, 
                    names=risk_counts.index,
                    title="CUSTOMER RISK SEGMENTATION",
                    color_discrete_sequence=['#FFD700', '#FFC700', '#FFB700'],
                    hole=0.4
                )
                
                fig.update_layout(
                    paper_bgcolor="#000000",
                    plot_bgcolor="#000000",
                    font={'color': "#FFD700", 'family': "Arial", 'size': 14},
                    title_font_color="#FFD700",
                    title_font_size=20,
                    showlegend=True,
                    legend=dict(
                        bgcolor="#1a1a1a",
                        bordercolor="#FFD700",
                        borderwidth=2,
                        font=dict(color="#FFD700")
                    )
                )
                
                fig.update_traces(
                    textposition='inside',
                    textinfo='percent+label',
                    textfont_size=14,
                    textfont_color='#000000',
                    marker=dict(line=dict(color='#000000', width=2))
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Top risk customers
                st.markdown("---")
                st.markdown("""
                    <div style='text-align: center; padding: 1rem; background-color: #000000;'>
                        <h2 style='color: #FFD700; font-size: 2rem;'>⚠️ TOP 20 HIGH-RISK CUSTOMERS</h2>
                    </div>
                """, unsafe_allow_html=True)
                
                top_risk = df_segmented.nlargest(20, 'churn_probability')[
                    ['churn_probability', 'risk_score', 'risk_tier', 'MonthlyCharges', 'tenure']
                ]
                
                # Format the dataframe
                top_risk_display = top_risk.copy()
                top_risk_display['churn_probability'] = top_risk_display['churn_probability'].apply(lambda x: f"{x*100:.1f}%")
                top_risk_display['MonthlyCharges'] = top_risk_display['MonthlyCharges'].apply(lambda x: f"₹{x:.2f}")
                
                st.dataframe(
                    top_risk_display,
                    use_container_width=True,
                    height=400
                )
                
                # Download results
                st.markdown("<br>", unsafe_allow_html=True)
                csv = df_segmented.to_csv(index=False)
                
                col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
                with col_btn2:
                    st.download_button(
                        label="📥 DOWNLOAD FULL RESULTS",
                        data=csv,
                        file_name="churn_predictions.csv",
                        mime="text/csv",
                        use_container_width=True
                    )

# Footer with yellow and black
st.markdown("---")
st.markdown("""
    <div style='text-align: center; padding: 2rem 0; background-color: #000000;'>
        <p style='margin: 0; font-size: 1rem; color: #FFD700; font-weight: 600;'>
            ⚡ Built with MLflow, FastAPI, and Streamlit | MLOps Best Practices
        </p>
        <p style='margin: 0.5rem 0 0 0; font-size: 0.9rem; color: #FFD700; opacity: 0.8;'>
            🚀 Production-Ready ML System with Business Impact Analysis
        </p>
    </div>
""", unsafe_allow_html=True)
