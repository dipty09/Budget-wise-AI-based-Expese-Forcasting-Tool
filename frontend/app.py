import streamlit as st
import requests
import pandas as pd
import os
import nltk
import uuid
from datetime import datetime
from nltk.tokenize import word_tokenize
nltk.download('punkt', quiet=True)

API_URL = "http://127.0.0.1:5000"
CSV_FILE = "../ml/data/budgetwise_finance_dataset_cleaned.csv"

st.title("💰 BudgetWise AI-Based Expense Forecasting Tool")
st.subheader("User Authentication & Advanced Transaction Input")

menu = ["Register", "Login", "Add Transaction"]
choice = st.sidebar.selectbox("Select Option", menu)

# ------------------------------------------------------------
# AUTO CATEGORIZATION LOGIC (NLTK)
# ------------------------------------------------------------
def auto_categorize(text):
    tokens = [word.lower() for word in word_tokenize(str(text))]
    categories = {
       "Food & Dining": ["restaurant", "food", "lunch", "dinner", "meal", "pizza", "burger", "cafe", "coffee"],
        "Transportation": ["bus", "train", "uber", "ola", "fuel", "petrol", "diesel", "ticket"],
        "Shopping": ["shopping", "mall", "clothes", "apparel", "store", "purchase"],
        "Utilities": ["electricity", "water", "gas", "internet", "mobile", "recharge", "bill"],
        "Health & Fitness": ["hospital", "medicine", "doctor", "gym", "pharmacy","Health"],
        "Entertainment": ["movie", "netflix", "amazon", "music", "game", "subscription"],
        "Education": ["school", "college", "course", "exam", "fee", "book"],
        "Salary / Income": ["salary", "income", "credit", "bonus", "deposit"],
        "Travel": ["travel", "flight", "hotel", "train", "uber", "ola", "bus", "booking", "airport"],
        "Rent & Housing": ["rent", "apartment", "lease", "tenant", "monthly rent"],
        "Investments & Savings": ["investment", "fixed deposit", "mutual fund", "stock", "savings", "fd"],
        "Loans & EMIs": ["emi", "loan", "installment", "credit payment", "debt"],
        "Charity & Donations": ["donation", "charity", "ngo", "fundraising"],
        "Personal Care": ["salon", "beauty", "spa", "makeup", "parlor"],
        "Insurance": ["insurance", "premium", "policy", "claim"],
        "Business & Freelance": ["freelance", "business", "consulting", "project", "contract"],
        "Household & Groceries": ["grocery", "market", "supermarket", "essentials", "household"],
        "Subscriptions & Services": ["spotify", "prime", "apple", "disney", "subscription", "membership"],
        "Financial Fees": ["bank charge", "fee", "commission", "tax", "service charge"],
        "Miscellaneous": ["misc", "others"]
    }

    
    for category, keywords in categories.items():
        if any(word in tokens for word in keywords):
            return category
    return "Other"

if choice == "Register":
    st.header("Register New User")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        try:
            res = requests.post(f"{API_URL}/auth/register", json={"email": email, "password": password})
            if res.status_code == 201:
                st.success(res.json().get("message", "Registered Successfully!"))
            else:
                st.error(res.json().get("error", "Registration Failed"))
        except Exception as e:
            st.error(f"⚠ Backend not reachable: {e}")

# ------------------------------------------------------------
# LOGIN
# ------------------------------------------------------------
elif choice == "Login":
    st.header("User Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        try:
            res = requests.post(f"{API_URL}/auth/login", json={"email": email, "password": password})
            if res.status_code == 200:
                st.session_state['token'] = res.json()['token']
                st.session_state['user_id'] = res.json().get('user_id', 'U001')
                st.success("✅ Login Successful!")
            else:
                st.error(res.json().get('error', 'Login Failed'))
        except Exception as e:
            st.error(f"⚠ Backend not reachable: {e}")


elif choice == "Add Transaction":
    st.header("➕ Add New Transaction")

    if 'token' not in st.session_state:
        st.warning("Please login first!")
    else:
        # -------- Input Fields --------
        transaction_type = st.selectbox("Transaction Type", ["Income", "Expense"])
        amount = st.number_input("Amount (₹)", min_value=0.0, step=0.01)
        payment_mode = st.selectbox("Payment Mode", ["Cash", "UPI", "Credit Card", "Debit Card", "Net Banking"])
        location = st.text_input("Location (optional)")
        description = st.text_area("Description / Notes")

        if st.button("Add Transaction"):
            # -------- Auto Fields --------
            transaction_id = str(uuid.uuid4())[:8].upper()
            user_id = st.session_state.get("user_id", "U001")
            category = auto_categorize(description)
            date = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
            month = datetime.now().strftime("%B")
            weekday = datetime.now().strftime("%A")
            year = datetime.now().year
            notes = description

            new_entry = {
                "transaction_id": transaction_id,
                "user_id": user_id,
                "transaction_type": transaction_type,
                "category": category,
                "amount": amount,
                "payment_mode": payment_mode,
                "location": location,
                "notes": notes,
                "month": month,
                "weekday": weekday,
                "year": year,
                "description": description,
                "date": date
            }

            # -------- (1) Save to CSV Locally --------
            try:
                if os.path.exists(CSV_FILE):
                    df = pd.read_csv(CSV_FILE)
                    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
                else:
                    df = pd.DataFrame([new_entry])
                df.to_csv(CSV_FILE, index=False)
                st.success(f"✅ Transaction ({category}) saved locally in CSV.")
            except Exception as e:
                st.error(f"Error saving to CSV: {e}")

            # -------- (2) Sync to Database --------
            try:
                headers = {"Authorization": st.session_state['token']}
                res = requests.post(f"{API_URL}/transaction/add", json=new_entry, headers=headers)
                if res.status_code == 201:
                    st.info("☁ Transaction synced to database successfully.")
                else:
                    st.warning("⚠ Could not sync to database (check backend).")
            except Exception as e:
                st.warning(f"Backend not reachable: {e}")

            # -------- (3) Frontend Update --------
            if os.path.exists(CSV_FILE):
                st.markdown("### 📊 Updated Transaction History")
                display_df = pd.read_csv(CSV_FILE)
                st.dataframe(display_df.tail(10), use_container_width=True)