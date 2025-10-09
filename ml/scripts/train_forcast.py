import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

# Load dataset
file_path = '../data/DatasetFinalCSV.csv'
df = pd.read_csv(file_path)

# ✅ Convert 'Month' column into a proper datetime column
# Assuming months are in order like "January", "February", ...
df['ds'] = pd.to_datetime(df['Month'] + ' 2024', format='%B %Y')  # change year if needed
df['y'] = df['AmountOfProduct']

# Select only Prophet-required columns
df = df[['ds', 'y']]

# Train Prophet model
model = Prophet()
model.fit(df)

# Forecast for next 6 months
future = model.make_future_dataframe(periods=6, freq='M')
forecast = model.predict(future)

# Save output
forecast.to_csv('../data/forecast_output.csv', index=False)

# Plot and save
fig1 = model.plot(forecast)
plt.title("Budget Forecasting for Next 6 Months")
plt.xlabel("Date")
plt.ylabel("Amount Spent")
plt.savefig('../data/forecast_plot.png')
plt.show()

print("✅ Forecast complete! Saved forecast_output.csv and forecast_plot.png.")