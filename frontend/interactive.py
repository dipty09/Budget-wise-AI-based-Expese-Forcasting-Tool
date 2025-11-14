# frontend/advanced_dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from prophet import Prophet
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title="BudgetWise — Advanced Dashboard", layout="wide")
st.title("BudgetWise — Advanced Financial Dashboard")

MASTER_CSV = os.getenv("MASTER_CSV_PATH")

# Load data
uploaded = st.sidebar.file_uploader("Upload master CSV (optional)", type=["csv"])
if uploaded:
    df = pd.read_csv(uploaded)
else:
    if not os.path.exists(MASTER_CSV):
        st.warning("Master CSV not found. Add transactions first or upload CSV.")
        st.stop()
    df = pd.read_csv(MASTER_CSV)

# ✅ Ensure date is always datetime
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df = df.dropna(subset=["date"])

# ✅ Ensure amount numeric
df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)

# ✅ Create transaction type if missing
if "transaction_type" not in df.columns:
    df["transaction_type"] = df["amount"].apply(lambda x: "Income" if x > 0 else "Expense")

# ✅ Fill missing categories
df["category"] = df["category"].fillna("Uncategorized")

# Sidebar Filters
st.sidebar.header("Filters & Controls")
start = st.sidebar.date_input("Start date", value=df["date"].min().date())
end = st.sidebar.date_input("End date", value=df["date"].max().date())
freq = st.sidebar.selectbox("Aggregation period", ["D", "W", "M"], index=2)
cat_list = ["All"] + sorted(df["category"].unique().tolist())
sel_cat = st.sidebar.selectbox("Category", cat_list)
tx_types = st.sidebar.multiselect("Transaction Type", options=df["transaction_type"].unique(), default=df["transaction_type"].unique())

# Apply filters
mask = (
    (df["date"] >= pd.Timestamp(start)) &
    (df["date"] <= pd.Timestamp(end)) &
    (df["transaction_type"].isin(tx_types))
)

if sel_cat != "All":
    mask &= (df["category"] == sel_cat)

df_f = df.loc[mask].copy()

# Top metrics
col1, col2, col3 = st.columns(3)
total_income = df_f[df_f["transaction_type"] == "Income"]["amount"].sum()
total_expense = df_f[df_f["transaction_type"] == "Expense"]["amount"].sum()
balance = total_income - total_expense

col1.metric("Total Income", f"₹{total_income:,.2f}")
col2.metric("Total Expense", f"₹{total_expense:,.2f}")
col3.metric("Net Balance", f"₹{balance:,.2f}")

st.markdown("---")

# Expense Pie Chart
st.subheader("Spending Breakdown by Category")
cat_summary = df_f[df_f["transaction_type"] == "Expense"].groupby("category")["amount"].sum().reset_index()
if not cat_summary.empty:
    fig = px.pie(cat_summary, names="category", values="amount", hole=0.4)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No expense data for selected filters.")

st.markdown("---")

# Income vs Expense Trend
st.subheader("Income vs Expense Trend")
trend = df_f.set_index("date").groupby([pd.Grouper(freq=freq), "transaction_type"])["amount"].sum().unstack(fill_value=0).reset_index()

fig2 = go.Figure()
if "Income" in trend.columns:
    fig2.add_trace(go.Scatter(x=trend["date"], y=trend["Income"], mode="lines+markers", name="Income"))
if "Expense" in trend.columns:
    fig2.add_trace(go.Scatter(x=trend["date"], y=trend["Expense"], mode="lines+markers", name="Expense"))
fig2.update_layout(title="Income vs Expense Trend")
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# Forecasting
st.subheader("Forecasted Cashflow (Prophet)")

forecast_cat = st.selectbox("Forecast category", ["All"] + sorted(df["category"].unique().tolist()))
horizon = st.slider("Forecast horizon (months)", 1, 12, 6)

if forecast_cat == "All":
    ts = df.groupby(pd.Grouper(key="date", freq="M"))["amount"].sum().reset_index().rename(columns={"date": "ds", "amount": "y"})
else:
    ts = df[df["category"] == forecast_cat].groupby(pd.Grouper(key="date", freq="M"))["amount"].sum().reset_index().rename(columns={"date": "ds", "amount": "y"})

if len(ts) >= 3:
    model = Prophet()
    model.fit(ts)
    future = model.make_future_dataframe(periods=horizon * 30, freq="D")
    forecast = model.predict(future)
    figf = px.line(forecast, x="ds", y="yhat", title=f"Forecast ({forecast_cat})")
    st.plotly_chart(figf, use_container_width=True)
else:
    st.info("Not enough data for forecasting.")

st.markdown("---")

# Goal Tracking
st.subheader("Goal Progress Tracking")
if "goals" not in st.session_state:
    st.session_state["goals"] = []

with st.expander("Create a new goal"):
    gname = st.text_input("Goal name")
    gtarget = st.number_input("Target amount (₹)", min_value=0.0)
    gsaved = st.number_input("Saved so far (₹)", min_value=0.0)
    gdate = st.date_input("Target date")
    if st.button("Add Goal"):
        st.session_state["goals"].append({"name": gname, "target": gtarget, "saved": gsaved, "date": str(gdate)})
        st.success("Goal added.")

for g in st.session_state["goals"]:
    progress = (g["saved"] / g["target"] * 100) if g["target"] > 0 else 0
    st.metric(g["name"], f"₹{g['saved']:,.2f} / ₹{g['target']:,.2f}", f"{progress:.1f}%")