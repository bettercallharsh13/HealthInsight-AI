import streamlit as st
import json
import pandas as pd
from datetime import datetime
from dataclasses import dataclass
from typing import Optional, List, Dict
import plotly.graph_objects as go
import plotly.express as px

# Constants
class HealthConstants:
    BMI_UNDERWEIGHT = 18.5
    BMI_NORMAL = 25.0
    BMI_OVERWEIGHT = 30.0
    SLEEP_RECOMMENDED = 7.0
    SLEEP_MAX = 9.0
    WATER_RECOMMENDED = 2.0
    AGE_MAX = 120
    WEIGHT_MAX = 300
    HEIGHT_MAX = 250
    WATER_MAX = 10
    SLEEP_MAX = 24

@dataclass
class User:
    name: str
    age: int
    height: float  # cm
    weight: float  # kg
    sleep: float   # hours
    water: float   # liters
    id: Optional[int] = None

    def __post_init__(self):
        """Validate data after initialization"""
        if self.age <= 0 or self.age > HealthConstants.AGE_MAX:
            raise ValueError(f"Age must be between 1 and {HealthConstants.AGE_MAX}")
        if self.weight <= 0 or self.weight > HealthConstants.WEIGHT_MAX:
            raise ValueError(f"Weight must be between 1 and {HealthConstants.WEIGHT_MAX} kg")
        if self.height <= 0 or self.height > HealthConstants.HEIGHT_MAX:
            raise ValueError(f"Height must be between 1 and {HealthConstants.HEIGHT_MAX} cm")
        if self.water < 0 or self.water > HealthConstants.WATER_MAX:
            raise ValueError(f"Water consumption should be between 0 and {HealthConstants.WATER_MAX}L")
        if self.sleep < 0 or self.sleep > HealthConstants.SLEEP_MAX:
            raise ValueError(f"Sleep hours must be between 0 and {HealthConstants.SLEEP_MAX}")

class HealthAnalyzer:
    def __init__(self, user):
        self.user = user

    def bmi(self) -> float:
        return self.user.weight / ((self.user.height / 100) ** 2)

    def bmi_status(self) -> str:
        bmi = self.bmi()
        if bmi < HealthConstants.BMI_UNDERWEIGHT:
            return "Underweight"
        elif bmi < HealthConstants.BMI_NORMAL:
            return "Normal weight"
        elif bmi < HealthConstants.BMI_OVERWEIGHT:
            return "Overweight"
        else:
            return "Obese"

    def health_score(self) -> int:
        score = 100
        bmi = self.bmi()

        if bmi < HealthConstants.BMI_UNDERWEIGHT:
            score -= (HealthConstants.BMI_UNDERWEIGHT - bmi) * 2
        elif bmi > HealthConstants.BMI_NORMAL:
            score -= (bmi - HealthConstants.BMI_NORMAL) * 2

        if self.user.sleep < HealthConstants.SLEEP_RECOMMENDED:
            score -= (HealthConstants.SLEEP_RECOMMENDED - self.user.sleep) * 3

        if self.user.water < HealthConstants.WATER_RECOMMENDED:
            score -= (HealthConstants.WATER_RECOMMENDED - self.user.water) * 5

        return max(0, min(100, score))

    def recommendations(self) -> List[str]:
        tips = []
        bmi = self.bmi()
        
        if bmi > HealthConstants.BMI_NORMAL:
            tips.append("🏃 Increase physical activity - aim for 30 minutes of moderate exercise daily.")
        elif bmi < HealthConstants.BMI_UNDERWEIGHT:
            tips.append("🍽️ Increase calorie intake through balanced meals. Consider consulting a nutritionist.")
        
        if self.user.sleep < HealthConstants.SLEEP_RECOMMENDED:
            tips.append(f"😴 Sleep at least {HealthConstants.SLEEP_RECOMMENDED} hours. Try going to bed {HealthConstants.SLEEP_RECOMMENDED - self.user.sleep:.0f} hours earlier.")
        
        if self.user.water < HealthConstants.WATER_RECOMMENDED:
            tips.append(f"💧 Drink more water - aim for {HealthConstants.WATER_RECOMMENDED}L daily. You're drinking {self.user.water:.1f}L.")
        
        return tips or ["✅ No major concerns! Maintain your healthy habits."]

    def ai_insight(self) -> str:
        insights = [f"📊 {self.user.name} has a BMI of {self.bmi():.1f}."]
        bmi = self.bmi()
        
        if bmi < HealthConstants.BMI_UNDERWEIGHT:
            insights.append("Consider gaining weight through a balanced diet.")
        elif bmi > HealthConstants.BMI_NORMAL:
            insights.append("Consider weight management through diet and exercise.")
        else:
            insights.append("Your BMI is in the healthy range.")
        
        if self.user.sleep < HealthConstants.SLEEP_RECOMMENDED:
            insights.append(f"Sleep {HealthConstants.SLEEP_RECOMMENDED - self.user.sleep:.1f} more hours per night.")
        elif self.user.sleep > HealthConstants.SLEEP_MAX:
            insights.append("You may be sleeping too much.")
        
        if self.user.water < HealthConstants.WATER_RECOMMENDED:
            insights.append(f"Drink {HealthConstants.WATER_RECOMMENDED - self.user.water:.1f}L more water daily.")
        
        return " ".join(insights)

    def get_trend_analysis(self, history: List[Dict]) -> Dict:
        if not history:
            return {"trend": "Insufficient data", "records_analyzed": 0}
        
        recent = history[-5:]  # Last 5 records
        scores = [h.get('score', 0) for h in recent]
        
        if len(scores) > 1:
            first_score = scores[0]
            last_score = scores[-1]
            
            if last_score > first_score:
                trend = "improving"
            elif last_score < first_score:
                trend = "declining"
            else:
                trend = "stable"
            
            return {
                "trend": trend,
                "current_score": last_score,
                "change": last_score - first_score,
                "records_analyzed": len(scores)
            }
        return {"trend": "stable", "records_analyzed": len(scores)}

def save_report(data: Dict) -> None:
    """Save health report to JSON file"""
    try:
        with open("history.json", "r") as file:
            history = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        history = []
    
    history.append(data)
    
    with open("history.json", "w") as file:
        json.dump(history, file, indent=2)

def load_history() -> List[Dict]:
    """Load health history from JSON file"""
    try:
        with open("history.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def create_bmi_gauge(bmi_value: float) -> go.Figure:
    """Create a BMI gauge chart"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=bmi_value,
        title={'text': "BMI"},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [None, 40]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 18.5], 'color': "lightblue"},
                {'range': [18.5, 25], 'color': "lightgreen"},
                {'range': [25, 30], 'color': "yellow"},
                {'range': [30, 40], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': bmi_value
            }
        }
    ))
    fig.update_layout(height=300)
    return fig

def plot_health_history(history: List[Dict]) -> go.Figure:
    """Create a line chart of health scores over time"""
    if not history:
        return None
    
    df = pd.DataFrame(history)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['score'],
        mode='lines+markers',
        name='Health Score',
        line=dict(color='blue', width=2),
        marker=dict(size=8)
    ))
    
    # Add reference line for perfect score
    fig.add_hline(y=100, line_dash="dash", line_color="green", 
                  annotation_text="Perfect Score")
    
    fig.update_layout(
        title="Health Score History",
        xaxis_title="Date",
        yaxis_title="Health Score",
        yaxis_range=[0, 105],
        height=400,
        hovermode='x'
    )
    return fig

def plot_bmi_history(history: List[Dict]) -> go.Figure:
    """Create a line chart of BMI over time"""
    if not history:
        return None
    
    df = pd.DataFrame(history)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['bmi'],
        mode='lines+markers',
        name='BMI',
        line=dict(color='orange', width=2),
        marker=dict(size=8)
    ))
    
    # Add reference lines for BMI categories
    fig.add_hline(y=18.5, line_dash="dash", line_color="blue", 
                  annotation_text="Underweight")
    fig.add_hline(y=25, line_dash="dash", line_color="green", 
                  annotation_text="Normal")
    fig.add_hline(y=30, line_dash="dash", line_color="red", 
                  annotation_text="Overweight")
    
    fig.update_layout(
        title="BMI History",
        xaxis_title="Date",
        yaxis_title="BMI",
        height=400,
        hovermode='x'
    )
    return fig

def display_bmi_info(bmi_value: float, status: str):
    """Display BMI information with appropriate styling"""
    colors = {
        "Underweight": "🔵",
        "Normal weight": "🟢",
        "Overweight": "🟡",
        "Obese": "🔴"
    }
    st.markdown(f"### {colors.get(status, '⚪')} BMI: {bmi_value:.1f} - {status}")

def main():
    st.set_page_config(
        page_title="Health Tracker Dashboard",
        page_icon="🏥",
        layout="wide"
    )
    
    # Custom CSS
    st.markdown("""
        <style>
        .main-header {
            text-align: center;
            padding: 1rem 0;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px;
            color: white;
            margin-bottom: 2rem;
        }
        .metric-card {
            background: #f0f2f6;
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Title
    st.markdown('<div class="main-header"><h1>🏥 Personal Health Tracker</h1></div>', unsafe_allow_html=True)
    
    # Sidebar for input
    with st.sidebar:
        st.header("📝 Health Data Entry")
        st.markdown("---")
        
        with st.form("health_form"):
            name = st.text_input("Full Name", max_chars=50)
            
            col1, col2 = st.columns(2)
            with col1:
                age = st.number_input("Age", min_value=1, max_value=120, value=30)
                weight = st.number_input("Weight (kg)", min_value=1.0, max_value=300.0, value=70.0, step=0.1)
                sleep = st.number_input("Sleep (hours)", min_value=0.0, max_value=24.0, value=8.0, step=0.5)
            with col2:
                height = st.number_input("Height (cm)", min_value=1.0, max_value=250.0, value=175.0, step=0.1)
                water = st.number_input("Water (liters)", min_value=0.0, max_value=10.0, value=2.0, step=0.1)
            
            submitted = st.form_submit_button("💾 Save Health Data")
        
        st.markdown("---")
        st.caption("Data is saved locally in history.json")
        
        # Clear history button
        if st.button("🗑️ Clear History", type="secondary"):
            if st.checkbox("Confirm clear all history?"):
                with open("history.json", "w") as f:
                    json.dump([], f)
                st.success("History cleared!")
                st.rerun()
    
    # Main content area
    if submitted and name:
        try:
            # Create user and analyzer
            user = User(name, age, height, weight, sleep, water)
            analyzer = HealthAnalyzer(user)
            
            # Save report
            report = {
                "date": str(datetime.now()),
                "name": user.name,
                "age": user.age,
                "height": user.height,
                "weight": user.weight,
                "sleep": user.sleep,
                "water": user.water,
                "bmi": round(analyzer.bmi(), 2),
                "status": analyzer.bmi_status(),
                "score": analyzer.health_score()
            }
            save_report(report)
            
            # Display current health metrics
            st.success(f"✅ Health data saved for {name}!")
            
            # Metrics Row
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("BMI", f"{analyzer.bmi():.1f}", analyzer.bmi_status())
            with col2:
                st.metric("Health Score", f"{analyzer.health_score()}/100")
            with col3:
                st.metric("Sleep", f"{sleep}h", "Recommended: 7-9h")
            with col4:
                st.metric("Water", f"{water}L", "Recommended: 2L")
            
            # BMI Gauge
            st.markdown("---")
            col1, col2 = st.columns([1, 2])
            with col1:
                st.plotly_chart(create_bmi_gauge(analyzer.bmi()), use_container_width=True)
            with col2:
                st.markdown("### 📊 Health Analysis")
                st.markdown(f"**BMI Status:** {analyzer.bmi_status()}")
                st.markdown(f"**Health Score:** {analyzer.health_score()}/100")
                
                # Progress bar for health score
                st.progress(analyzer.health_score() / 100)
                
                # AI Insights
                st.markdown("### 🤖 AI Insights")
                st.info(analyzer.ai_insight())
            
            # Recommendations
            st.markdown("---")
            st.markdown("### 💡 Recommendations")
            recommendations = analyzer.recommendations()
            if recommendations:
                for tip in recommendations:
                    st.write(tip)
            else:
                st.success("✅ No recommendations needed. Keep up the good work!")
            
        except ValueError as e:
            st.error(f"❌ Error: {str(e)}")
    
    elif submitted and not name:
        st.warning("⚠️ Please enter your name.")
    
    # Display history
    st.markdown("---")
    st.markdown("## 📈 Health History")
    
    history = load_history()
    
    if history:
        # Filters
        col1, col2 = st.columns(2)
        with col1:
            show_last = st.selectbox("Show last N records", [10, 25, 50, "All"], index=0)
        
        # Display history table
        df_history = pd.DataFrame(history)
        df_history['date'] = pd.to_datetime(df_history['date'])
        
        if show_last != "All":
            df_history = df_history.tail(show_last)
        
        # Charts
        col1, col2 = st.columns(2)
        with col1:
            score_fig = plot_health_history(df_history.to_dict('records'))
            if score_fig:
                st.plotly_chart(score_fig, use_container_width=True)
        
        with col2:
            bmi_fig = plot_bmi_history(df_history.to_dict('records'))
            if bmi_fig:
                st.plotly_chart(bmi_fig, use_container_width=True)
        
        # History table with styling
        st.markdown("### 📋 Detailed History")
        display_df = df_history.copy()
        display_df['date'] = display_df['date'].dt.strftime('%Y-%m-%d %H:%M')
        display_df = display_df[['date', 'name', 'bmi', 'status', 'score']]
        display_df.columns = ['Date', 'Name', 'BMI', 'Status', 'Score']
        
        
        
        
        st.dataframe(display_df, use_container_width=True)
        
        # Trend Analysis
        if len(history) > 1:
            st.markdown("### 📊 Trend Analysis")
                     # Use the latest record to create a User object
            latest_record = history[-1]
            
            # Create user from stored data (or use defaults if missing)
            user_data = User(
                name=latest_record.get('name', 'User'),
                age=latest_record.get('age', 30),
                height=latest_record.get('height', 175.0),
                weight=latest_record.get('weight', 70.0),
                sleep=latest_record.get('sleep', 8.0),
                water=latest_record.get('water', 2.0)
            )
            analyzer_latest = HealthAnalyzer(user_data)
            trend = analyzer_latest.get_trend_analysis(history)
            
            if trend.get('records_analyzed', 0) > 1:
                col1, col2, col3 = st.columns(3)
                with col1:
                    trend_emoji = "📈" if trend['trend'] == "improving" else "📉" if trend['trend'] == "declining" else "➡️"
                    st.metric("Trend", f"{trend_emoji} {trend['trend'].title()}")
                with col2:
                    st.metric("Current Score", trend.get('current_score', 0))
                with col3:
                    change = trend.get('change', 0)
                    # FIXED: Properly format the change value
                    if isinstance(change, float):
                        change_str = f"{change:+.1f}"
                    else:
                        change_str = f"{change:+d}"
                    st.metric("Change", f"{change_str} points")

                             
        
        # Export options
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📥 Export as CSV"):
                csv = display_df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"health_history_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
    
    else:
        st.info("📭 No health data recorded yet. Enter your health metrics above to get started!")

if __name__ == "__main__":
    main()
