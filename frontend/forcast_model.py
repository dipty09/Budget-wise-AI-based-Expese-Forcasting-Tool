# frontend/forecast_model.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet
from datetime import datetime

# --- Streamlit Page Config ---
st.set_page_config(page_title="Forecasting Dashboard", page_icon="📈", layout="wide")

# --- Title and Description ---
st.markdown("<h1 style='text-align: center; color: #2E86C1;'>📊 Expense Forecasting & Financial Goal Setting</h1>", unsafe_allow_html=True)
st.write("This module analyzes your past expense trends and predicts future spending patterns using *Meta’s Prophet Model*.")

# --- File Upload Section ---
uploaded_file = st.file_uploader("📤 Upload your categorized expense CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # --- Data Validation ---
    if 'date' not in df.columns or 'amount' not in df.columns:
        st.error("CSV must include 'date' and 'amount' columns.")
        st.stop()

    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date', 'amount'])
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')

    # --- Select Category if available ---
    category = None
    if 'category' in df.columns:
        category = st.selectbox("Select Category for Forecasting:", df['category'].unique())
        filtered_df = df[df['category'] == category]
    else:
        filtered_df = df.copy()

    # --- Aggregate Data by Date ---
    forecast_df = filtered_df.groupby('date')['amount'].sum().reset_index()
    forecast_df.columns = ['ds', 'y']

    # --- Prophet Forecasting ---
    model = Prophet(daily_seasonality=True, yearly_seasonality=True)
    model.fit(forecast_df)

    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)

    # --- Visualization ---
    st.subheader(f"📅 Forecast Results for {category if category else 'All Expenses'}")

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(forecast_df['ds'], forecast_df['y'], label='Actual Expenses', color='#1A5276', marker='o')
    ax.plot(forecast['ds'], forecast['yhat'], label='Forecasted Expenses', color='#117A65', linestyle='--')
    ax.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], color='#D6EAF8', alpha=0.3)
    ax.set_xlabel("Date")
    ax.set_ylabel("Expense Amount")
    ax.legend()
    st.pyplot(fig)

    # --- Goal Setting Section ---
    st.markdown("---")
    st.markdown("<h3 style='color: #2874A6;'>🎯 Financial Goal Setting</h3>", unsafe_allow_html=True)
    goal_text = st.text_input("Define your goal (e.g., Save ₹5000 by end of the month):")
    target_amount = st.number_input("Target Saving/Reduction Amount:", min_value=0.0, step=100.0)
    target_date = st.date_input("Target Date:", datetime.now())

    if st.button("Set Goal"):
        st.success(f"Goal Set Successfully: {goal_text}")
        st.info(f"🎯 Target: ₹{target_amount} by {target_date.strftime('%d %B %Y')}")

    # --- Data Export Option ---
    if st.button("📥 Download Forecast Data"):
        forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_csv("forecast_results.csv", index=False)
        st.success("Forecast results saved as 'forecast_results.csv'.")

else:
    st.warning("⚠ Please upload your categorized CSV file to begin forecasting.")