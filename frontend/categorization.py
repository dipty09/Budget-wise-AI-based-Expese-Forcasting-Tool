import streamlit as st
import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import plotly.express as px

# Download necessary NLP resources
nltk.download("punkt")
nltk.download("stopwords")

# ---------- NLP Preprocessing ----------
def preprocess_text(text):
    if pd.isna(text):
        return ""
    text = re.sub(r"[^a-zA-Z\s]", "", str(text))
    tokens = word_tokenize(text.lower())
    filtered = [w for w in tokens if w not in stopwords.words("english")]
    return " ".join(filtered)

# ---------- Categorization Function ----------
def categorize_transaction(note, txn_type):
    text = preprocess_text(str(note)) + " " + str(txn_type).lower()

    categories = {
        "Food & Dining": ["restaurant", "food", "lunch", "dinner", "meal", "pizza", "burger", "cafe"],
        "Transportation": ["bus", "train", "uber", "ola", "fuel", "petrol", "diesel", "ticket"],
        "Shopping": ["shopping", "mall", "clothes", "apparel", "store", "purchase"],
        "Utilities": ["electricity", "water", "gas", "internet", "mobile", "recharge", "bill"],
        "Health & Fitness": ["hospital", "medicine", "doctor", "gym", "pharmacy"],
        "Entertainment": ["movie", "netflix", "amazon", "music", "game", "subscription"],
        "Education": ["school", "college", "course", "exam", "fee", "book"],
        "Salary / Income": ["salary", "income", "credit", "bonus", "deposit"],
        "Others": []
    }

    for category, keywords in categories.items():
        if any(keyword in text for keyword in keywords):
            return category
    return "Others"

# ---------- Streamlit UI ----------
st.set_page_config(page_title="Expense Categorization Dashboard", layout="wide")

st.title("💰 Automated Expense Categorization Dashboard")

uploaded_file = st.file_uploader("📂 Upload your expense CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Handle missing columns
    required_cols = ["date", "notes", "transaction_type", "amount"]
    for col in required_cols:
        if col not in df.columns:
            st.error(f"❌ Missing required column: '{col}' in uploaded CSV.")
            st.stop()

    # Convert and validate data
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["notes"] = df["notes"].fillna("").astype(str)
    df["transaction_type"] = df["transaction_type"].fillna("").astype(str)
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)

    # Categorize transactions
    with st.spinner("🔍 Categorizing transactions using NLP..."):
        df["auto_category"] = df.apply(lambda x: categorize_transaction(x["notes"], x["transaction_type"]), axis=1)

    st.success("✅ Transactions categorized successfully!")

    # ---------- Display categorized table first ----------
    st.subheader("📋 Categorized Transactions")
    st.dataframe(
        df[["date", "notes", "transaction_type", "amount", "auto_category"]],
        use_container_width=True
    )

    # ---------- Pie chart visualization ----------
    st.subheader("📊 Expense Distribution by Category")

    category_summary = df.groupby("auto_category")["amount"].sum().reset_index()

    pie_fig = px.pie(
        category_summary,
        names="auto_category",
        values="amount",
        title="Expense Breakdown by Category",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    st.plotly_chart(pie_fig, use_container_width=True)

else:
    st.info("📤 Please upload your expense CSV file to begin.")