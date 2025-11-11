import streamlit as st
import pandas as pd
import os

class AdminDashboard:
    def run(self):
        st.title("🛠 Admin Dashboard")
        st.markdown("---")

        st.subheader("📊 Manage Transaction Categories")
        if os.path.exists("../ml/data/forecast_results.csv"):
            df = pd.read_csv("../ml/data/forecast_results.csv")
            st.write(df.head())
        else:
            st.warning("No forecast data found. Please run forecasting first.")

        st.subheader("⚙ Manage System Settings")
        st.text_input("Add New Category")
        st.button("Save Category")

        st.subheader("📈 System Monitoring")
        st.write("System is running normally ✅")

if __name__ == "_main_":
    admin = AdminDashboard()
    admin.run()