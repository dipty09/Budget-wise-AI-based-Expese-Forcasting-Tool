import streamlit as st
import requests

API_URL = "http://127.0.0.1:5000"

st.title("💰 BudgetWise AI-Based Expense Forecasting Tool")
st.subheader("User Authentication & Transaction Input")

menu = ["Register", "Login", "Add Transaction"]
choice = st.sidebar.selectbox("Select Option", menu)

if choice == "Register":
    st.header("Register New User")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        res = requests.post(f"{API_URL}/auth/register", json={"email": email, "password": password})
        st.success(res.json().get("message", "Registered Successfully!"))

elif choice == "Login":
    st.header("User Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        res = requests.post(f"{API_URL}/auth/login", json={"email": email, "password": password})
        if res.status_code == 200:
            st.session_state['token'] = res.json()['token']
            st.success("Login Successful!")
        else:
            st.error(res.json().get('error', 'Login Failed'))

elif choice == "Add Transaction":
    st.header("Add Transaction")
    if 'token' not in st.session_state:
        st.warning("Please login first!")
    else:
        date = st.date_input("Date")
        amount = st.number_input("Amount")
        category = st.text_input("Category")
        description = st.text_area("Description")
        if st.button("Add Transaction"):
            headers = {"Authorization": st.session_state['token']}
            data = {"date": str(date), "amount": amount, "category": category, "description": description}
            res = requests.post(f"{API_URL}/transaction/add", json=data, headers=headers)
            st.success(res.json().get("message", "Transaction added successfully"))