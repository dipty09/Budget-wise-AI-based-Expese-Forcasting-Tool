# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# -----------------------------
# Step 1: Load cleaned dataset
# -----------------------------
cleaned_csv_path = r"D:\Budget Expense_tool\budget-wise-ai-based-expese-forcasting-tool\ml\processed_data\budgetwise_finance_dataset_cleaned.csv"

df = pd.read_csv(cleaned_csv_path)
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

# -----------------------------
# Step 2: Streamlit Page Config
# -----------------------------
st.set_page_config(page_title="BudgetWise Expense Dashboard", layout="wide")
st.title("BudgetWise Expense Forecasting - Dashboard")

# -----------------------------
# Step 3: Sidebar Filters
# -----------------------------
years = df['year'].sort_values().unique()
selected_year = st.sidebar.selectbox("Select Year", years)

categories = df['category'].unique()
selected_categories = st.sidebar.multiselect("Select Categories", categories, default=categories)

# Filter data based on selections
filtered_df = df[(df['year'] == selected_year) & (df['category'].isin(selected_categories))]

# -----------------------------
# Step 4: Show summary statistics
# -----------------------------
st.subheader(f"Summary Statistics for {selected_year}")
st.write(filtered_df.describe())

# -----------------------------
# Step 5: Category-wise spending
# -----------------------------
st.subheader("Category-wise Total Spending")
category_sum = filtered_df.groupby('category')['amount'].sum().sort_values(ascending=False)
st.bar_chart(category_sum)

# -----------------------------
# Step 6: Monthly spending trend
# -----------------------------
st.subheader("Monthly Spending Trend")
monthly_sum = filtered_df.groupby('month')['amount'].sum().sort_index()

plt.figure(figsize=(10, 4))
sns.lineplot(x=monthly_sum.index, y=monthly_sum.values, marker='o')
plt.xticks(range(1, 13))
plt.xlabel("Month")
plt.ylabel("Total Amount")
plt.title(f"Monthly Spending in {selected_year}")
st.pyplot(plt)

# -----------------------------
# Step 7: Show raw data (optional)
# -----------------------------
st.subheader("Raw Data")
st.dataframe(filtered_df)