"""
Business Impact Calculator
Phase 4: Converting Predictions to Business Value
"""
import pandas as pd
import numpy as np

class BusinessImpactCalculator:
    """Calculate business metrics from churn predictions"""
    
    def __init__(self, avg_revenue_per_customer=70, 
                 retention_campaign_cost=10,
                 retention_success_rate=0.3):
        """
        Args:
            avg_revenue_per_customer: Average monthly revenue per customer (₹)
            retention_campaign_cost: Cost to run retention campaign per customer (₹)
            retention_success_rate: Success rate of retention campaigns (0-1)
        """
        self.avg_revenue = avg_revenue_per_customer
        self.campaign_cost = retention_campaign_cost
        self.success_rate = retention_success_rate
    
    def calculate_risk_score(self, churn_probability):
        """Convert churn probability to risk score (0-100)"""
        return int(churn_probability * 100)
    
    def assign_risk_tier(self, churn_probability):
        """Assign customer to risk tier"""
        if churn_probability >= 0.7:
            return "Critical Risk"
        elif churn_probability >= 0.4:
            return "Medium Risk"
        else:
            return "Low Risk"
    
    def calculate_customer_lifetime_value(self, monthly_charges, tenure):
        """Estimate customer lifetime value"""
        # Simple CLV: monthly charges * expected remaining tenure
        expected_remaining_months = max(24 - tenure, 12)
        return monthly_charges * expected_remaining_months

    
    def calculate_revenue_at_risk(self, df_with_predictions):
        """Calculate total revenue at risk from predicted churners"""
        high_risk = df_with_predictions[df_with_predictions['churn_probability'] >= 0.5]
        
        if 'MonthlyCharges' in high_risk.columns:
            # Annual revenue at risk
            revenue_at_risk = high_risk['MonthlyCharges'].sum() * 12
        else:
            # Use average if MonthlyCharges not available
            revenue_at_risk = len(high_risk) * self.avg_revenue * 12
        
        return revenue_at_risk
    
    def calculate_intervention_roi(self, df_with_predictions, top_n=None):
        """Calculate ROI of retention intervention"""
        
        # Sort by churn probability
        df_sorted = df_with_predictions.sort_values('churn_probability', ascending=False)
        
        if top_n:
            df_sorted = df_sorted.head(top_n)
        else:
            # Target high-risk customers (probability >= 0.5)
            df_sorted = df_sorted[df_sorted['churn_probability'] >= 0.5]
        
        n_customers = len(df_sorted)
        
        if n_customers == 0:
            return {
                'customers_targeted': 0,
                'intervention_cost': 0,
                'expected_revenue_saved': 0,
                'net_benefit': 0,
                'roi_percentage': 0
            }
        
        # Calculate costs and benefits
        intervention_cost = n_customers * self.campaign_cost
        
        if 'MonthlyCharges' in df_sorted.columns:
            potential_revenue = df_sorted['MonthlyCharges'].sum() * 12
        else:
            potential_revenue = n_customers * self.avg_revenue * 12
        
        expected_revenue_saved = potential_revenue * self.success_rate
        net_benefit = expected_revenue_saved - intervention_cost
        roi_percentage = (net_benefit / intervention_cost * 100) if intervention_cost > 0 else 0
        
        return {
            'customers_targeted': n_customers,
            'intervention_cost': intervention_cost,
            'expected_revenue_saved': expected_revenue_saved,
            'net_benefit': net_benefit,
            'roi_percentage': roi_percentage
        }

    
    def segment_customers(self, df_with_predictions):
        """Segment customers by risk tier"""
        df = df_with_predictions.copy()
        df['risk_score'] = df['churn_probability'].apply(self.calculate_risk_score)
        df['risk_tier'] = df['churn_probability'].apply(self.assign_risk_tier)
        
        # Summary by tier
        summary = df.groupby('risk_tier').agg({
            'churn_probability': ['count', 'mean'],
            'MonthlyCharges': 'sum' if 'MonthlyCharges' in df.columns else 'count'
        }).round(2)
        
        return df, summary
    
    def recommend_action(self, churn_probability, customer_value=None):
        """Recommend intervention action based on risk and value"""
        risk_tier = self.assign_risk_tier(churn_probability)
        
        if risk_tier == "Critical Risk":
            if customer_value and customer_value > 2000:
                return "Immediate personal outreach + premium retention offer"
            else:
                return "Automated retention campaign + discount offer"
        elif risk_tier == "Medium Risk":
            return "Proactive engagement + service upgrade offer"
        else:
            return "Standard engagement + loyalty program"
    
    def generate_business_report(self, df_with_predictions, top_n=500):
        """Generate comprehensive business impact report"""
        
        # Segment customers
        df_segmented, tier_summary = self.segment_customers(df_with_predictions)
        
        # Calculate metrics
        total_revenue_at_risk = self.calculate_revenue_at_risk(df_segmented)
        roi_metrics = self.calculate_intervention_roi(df_segmented, top_n=top_n)
        
        report = {
            'total_customers': len(df_segmented),
            'high_risk_customers': len(df_segmented[df_segmented['churn_probability'] >= 0.7]),
            'medium_risk_customers': len(df_segmented[
                (df_segmented['churn_probability'] >= 0.4) & 
                (df_segmented['churn_probability'] < 0.7)
            ]),
            'total_revenue_at_risk': total_revenue_at_risk,
            'intervention_plan': roi_metrics,
            'tier_summary': tier_summary
        }
        
        return report, df_segmented
