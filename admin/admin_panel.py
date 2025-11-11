import streamlit as st
import requests

BASE = "http://127.0.0.1:5000/admin"

st.set_page_config(page_title="Admin Panel", layout="wide")
st.title("⚙ System Administration Dashboard")

menu = st.sidebar.radio("Navigation", ["Dashboard Overview", "Manage Categories", "Manage Users", "Login Activity", "System Monitoring"])

# ----- Overview ----- #
if menu == "Dashboard Overview":
    st.header("📊 System Metrics Overview")
    metrics = requests.get(f"{BASE}/metrics").json()
    st.write(metrics)

# ----- Manage Categories ----- #
elif menu == "Manage Categories":
    st.header("📂 Category Management")
    data = requests.get(f"{BASE}/categories").json()

    for c in data:
        col1, col2 = st.columns([3,1])
        col1.write(c["name"])
        if col2.button("Delete", key=f"d{c['id']}"):
            requests.delete(f"{BASE}/categories/{c['id']}", json={"user": "admin"})
            st.rerun()

    new_cat = st.text_input("New Category")
    if st.button("Add Category"):
        requests.post(f"{BASE}/categories", json={"name": new_cat, "user": "admin"})
        st.rerun()

# ----- Manage Users (From Admin DB) ----- #
elif menu == "Manage Users":
    st.header("👥 User Management (Registered Users)")
    users = requests.get(f"{BASE}/users").json()

    for u in users:
        col1, col2, col3 = st.columns([3,2,2])
        # name may be null, fallback to email
        display_name = u.get("name") if u.get("name") else u["email"]
        col1.write(display_name)

        new_status = col2.selectbox("Status", ["active", "inactive"], index=["active","inactive"].index(u.get("status","active")), key=u["id"])
        if col3.button("Update", key=f"u{u['id']}"):
            requests.put(f"{BASE}/users/{u['id']}", json={"status": new_status, "user": "admin"})
            st.rerun()

# ----- Login Activity Log ----- #
elif menu == "Login Activity":
    st.header("🟢 User Login History")
    logs = requests.get(f"{BASE}/login-activity").json()

    for log in logs:
        st.write(f"{log['email']}** logged in at *{log['login_time']}*")

# ----- System Monitoring ----- #
elif menu == "System Monitoring":
    st.header("🖥 System Logs & Activity")
    logs = requests.get(f"{BASE}/logs").json()
    st.write(logs)