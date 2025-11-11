import streamlit as st
import pandas as pd
from prophet import Prophet
from datetime import datetime
import plotly.express as px
import os

# ------------------------------------------------------------
# Streamlit Page Configuration
# ------------------------------------------------------------
st.set_page_config(page_title="Expense Forecasting & Financial Goal Setting", layout="wide")
st.markdown(
    """
    <style>
    .main {background-color: #f8fafc;}
    .stButton>button {
        background-color: #0078D7;
        color: white;
        border-radius: 8px;
        height: 3em;
        width: 12em;
        font-size: 16px;
    }
    h1, h2, h3, h4 {color: #2E4053;}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("💹 AI-based Expense Forecasting & Goal Setting Tool")
st.markdown("---")

# ------------------------------------------------------------
# Upload Historical Data
# ------------------------------------------------------------
st.subheader("📂 Upload Historical Expense Data (Categorized CSV)")
uploaded_file = st.file_uploader("Upload your categorized expense file (.csv)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    required_columns = ["date", "amount", "auto_category", "transaction_type"]
    if not all(col in df.columns for col in required_columns):
        st.error("❌ Uploaded file must contain: date, amount, auto_category, transaction_type")
        st.stop()

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)

    st.success("✅ File uploaded successfully!")
    st.write("Here’s a preview of your dataset:")
    st.dataframe(df.head(), use_container_width=True)

    # ------------------------------------------------------------
    # Goal Setting
    # ------------------------------------------------------------
    st.markdown("### 🎯 Set Your Financial Goal")
    with st.form("goal_form"):
        goal_name = st.text_input("Goal Name (e.g., Emergency Fund, Travel Plan)")
        target_amount = st.number_input("Target Amount (₹)", min_value=0.0)
        target_date = st.date_input("Target Date")
        current_amount = st.number_input("Current Saved Amount (₹)", min_value=0.0)
        create_goal = st.form_submit_button("Create Goal")

    if create_goal:
        remaining_days = (target_date - datetime.now().date()).days
        remaining_amount = target_amount - current_amount
        daily_saving_req = remaining_amount / remaining_days if remaining_days > 0 else 0

        st.success(f"🎯 Goal '{goal_name}' created successfully!")
        st.write(f"📅 Target Date: {target_date.strftime('%d-%b-%Y')}")
        st.write(f"💰 Target: ₹{target_amount:,.2f}")
        st.write(f"💵 Current Savings: ₹{current_amount:,.2f}")
        st.info(f"To reach your goal, save approximately ₹{daily_saving_req:,.2f} per day.")

    st.markdown("---")

    # ------------------------------------------------------------
    # Data Preparation
    # ------------------------------------------------------------
    st.subheader("🧮 Historical Data Preparation")
    agg_option = st.selectbox("Select Aggregation Frequency", ["Monthly", "Weekly"])
    freq = "M" if agg_option == "Monthly" else "W"

    txn_filter = st.radio("Filter Transaction Type", ["All", "Income", "Expense"], horizontal=True)
    if txn_filter != "All":
        df = df[df["transaction_type"].str.lower() == txn_filter.lower()]

    df_agg = df.groupby([pd.Grouper(key="date", freq=freq), "auto_category"])["amount"].sum().reset_index()
    df_agg = df_agg.rename(columns={"date": "ds", "amount": "y"})

    st.success(f"✅ Data aggregated successfully ({agg_option} basis).")
    st.dataframe(df_agg.head(), use_container_width=True)
    st.markdown("---")

    # ------------------------------------------------------------
    # Forecasting Section
    # ------------------------------------------------------------
    st.subheader("📈 Prophet Forecast Visualization")
    category_list = df_agg["auto_category"].unique().tolist()
    selected_category = st.selectbox("Select Category to Forecast", category_list)
    forecast_months = st.slider("Forecast Period (Months)", 1, 12, 6)

    df_cat = df_agg[df_agg["auto_category"] == selected_category][["ds", "y"]]

    if len(df_cat) < 5:
        st.warning("⚠ Not enough data points for forecasting.")
    else:
        model = Prophet()
        model.fit(df_cat)

        # Ensure data covers up to today
        last_date = df_cat["ds"].max()
        today = pd.to_datetime(datetime.today().date())
        if last_date < today:
            missing_days = pd.date_range(start=last_date + pd.Timedelta(days=1), end=today)
            filler = pd.DataFrame({"ds": missing_days, "y": [0] * len(missing_days)})
            df_cat = pd.concat([df_cat, filler])

        # Forecast future
        future = model.make_future_dataframe(periods=forecast_months * 30, freq="D")
        forecast = model.predict(future)

        # Visualization
        st.markdown(f"#### 📊 Expense Forecast for {selected_category}")
        forecast_display = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]
        forecast_display["Type"] = "Forecast"

        actual_display = df_cat.rename(columns={"y": "yhat"})
        actual_display["yhat_lower"] = actual_display["yhat_upper"] = None
        actual_display["Type"] = "Actual"

        combined = pd.concat([actual_display, forecast_display], ignore_index=True)

        fig = px.line(
            combined,
            x="ds",
            y="yhat",
            color="Type",
            title=f"Expense Forecast Trend for {selected_category} ({agg_option})",
            labels={"ds": "Date", "yhat": "Amount (₹)"},
            color_discrete_map={"Actual": "#2E86C1", "Forecast": "#F39C12"}
        )

        fig.update_traces(mode="lines+markers")
        fig.update_layout(template="plotly_white", showlegend=True, height=500)
        st.plotly_chart(fig, use_container_width=True)

        # Summary
        st.markdown("### 📋 Forecast Summary")
        col1, col2, col3 = st.columns(3)
        col1.metric("Average Historical Amount", f"₹{df_cat['y'].mean():,.2f}")
        col2.metric("Projected Monthly Avg", f"₹{forecast['yhat'].mean():,.2f}")
        col3.metric("Forecast Period", f"{forecast_months} months")

        # Save forecast data
        os.makedirs("ml/data", exist_ok=True)
        forecast.to_csv("ml/data/forecast_results.csv", index=False)
        st.success("✅ Forecast results saved successfully!")

else:
    st.info("Please upload your categorized expense file to begin forecasting and goal setting.")