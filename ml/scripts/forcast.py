import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="AI Budget Forecast Tool", layout="wide")

st.title("💰 AI-Based Budget Forecasting Dashboard")

uploaded_file = st.file_uploader("📤 Upload your expense CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("✅ File uploaded successfully!")

        # Normalize column names
        df.columns = [col.strip().lower() for col in df.columns]

        # Detect relevant columns
        possible_date_cols = ['date', 'day', 'transaction_date']
        possible_amount_cols = ['amount', 'expense', 'spent', 'cost', 'price']

        date_col = next((col for col in possible_date_cols if col in df.columns), None)
        amount_col = next((col for col in possible_amount_cols if col in df.columns), None)

        if not date_col or not amount_col:
            st.error("⚠ Could not detect Date or Amount column. Please rename appropriately.")
        else:
            # Convert Date column
            df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
            df = df.dropna(subset=[date_col])

            # Clean the Amount column: remove currency symbols, commas, text
            df[amount_col] = (
                df[amount_col]
                .astype(str)
                .str.replace(r"[^\d\.\-]", "", regex=True)  # keep only digits, dots, and minus
            )

            # Convert safely to float
            df[amount_col] = pd.to_numeric(df[amount_col], errors='coerce')
            df = df.dropna(subset=[amount_col])

            # Group by day
            daily_expense = df.groupby(date_col)[amount_col].sum().reset_index()
            daily_expense = daily_expense.sort_values(by=date_col)

            # Display table
            st.subheader("📅 Daily Expense Summary")
            st.dataframe(daily_expense)

            # Daily trend chart
            st.subheader("📊 Daily Expense Trend")
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(daily_expense[date_col], daily_expense[amount_col], marker='o', linestyle='-')
            ax.set_title("Daily Expenses Over Time")
            ax.set_xlabel("Date")
            ax.set_ylabel("Expense (₹)")
            plt.xticks(rotation=45)
            st.pyplot(fig)

            # Forecast
            st.subheader("🤖 AI Forecast (Next 7 Days)")
            window_size = st.slider("Select moving average window size", 3, 10, 5)

            daily_expense['forecast'] = daily_expense[amount_col].rolling(window=window_size).mean()

            last_known = daily_expense[amount_col].iloc[-window_size:]
            forecast_values = [last_known.mean()] * 7
            future_dates = pd.date_range(
                daily_expense[date_col].iloc[-1] + pd.Timedelta(days=1), periods=7
            )

            forecast_df = pd.DataFrame({date_col: future_dates, 'forecasted_amount': forecast_values})
            st.write(forecast_df)

            # Combined visualization
            fig2, ax2 = plt.subplots(figsize=(10, 4))
            ax2.plot(daily_expense[date_col], daily_expense[amount_col], label="Actual")
            ax2.plot(forecast_df[date_col], forecast_df['forecasted_amount'], 'r--', label="Forecast")
            ax2.legend()
            ax2.set_title("Expense Forecast")
            plt.xticks(rotation=45)
            st.pyplot(fig2)

    except Exception as e:
        st.error(f"🚫 Error reading file: {e}")
else:
    st.info("📂 Please upload your expense CSV to start analysis.")