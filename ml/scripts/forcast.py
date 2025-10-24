import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
import os

# Automatically detect current working directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")

data_path = os.path.join(DATA_DIR, "budgetwise_finance_dataset_cleaned.csv")
forecast_output = os.path.join(DATA_DIR, "forecast_results.csv")

# Debug check
print("🔍 Looking for data file at:", data_path)

# --- Check if dataset exists ---
if not os.path.exists(data_path):
    raise FileNotFoundError(f"❌ Dataset not found at {data_path}. Please ensure the cleaned_expense_data.csv file exists.")

# Load the cleaned dataset
df = pd.read_csv(data_path)

# Ensure correct column naming for Prophet
df.rename(columns={"date": "ds", "amount": "y"}, inplace=True)

# Aggregate data by month for stable forecasting
df["ds"] = pd.to_datetime(df["ds"])
monthly_data = df.groupby(pd.Grouper(key="ds", freq="M")).sum().reset_index()

# Initialize Prophet model
model = Prophet()
model.fit(monthly_data)

# Create future dataframe (next 6 months)
future = model.make_future_dataframe(periods=6, freq="M")

# Generate forecast
forecast = model.predict(future)

# Save forecast results
forecast.to_csv(forecast_output, index=False)

# Visualization
plt.figure(figsize=(10, 5))
plt.plot(monthly_data["ds"], monthly_data["y"], label="Actual", marker='o')
plt.plot(forecast["ds"], forecast["yhat"], label="Forecast", linestyle="--")
plt.fill_between(forecast["ds"], forecast["yhat_lower"], forecast["yhat_upper"], color="gray", alpha=0.3)
plt.xlabel("Date")
plt.ylabel("Expenses (₹)")
plt.title("Expense Forecast - Next 6 Months")
plt.legend()
plt.tight_layout()

# Save forecast plot
plot_path = os.path.join(DATA_DIR, "forecast_plot.png")
plt.savefig(plot_path)
plt.show()

print("✅ Forecast generated successfully!")
print("📂 Forecast saved to:", forecast_output)
print("🖼 Plot saved to:", plot_path)