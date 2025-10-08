import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
import os

# Load dataset
file_path = os.path.join(os.path.dirname(__file__), '../data/DatasetFinalCSV.csv')
df = pd.read_csv(file_path)

# If no date column, create one
if 'Date' not in df.columns:
    df['Date'] = pd.date_range(start='2025-01-01', periods=len(df), freq='M')

# Aggregate monthly totals (or use original if one row per month)
monthly = df.groupby(pd.Grouper(key='Date', freq='M'))['AmountOfProduct'].sum().reset_index()

# Prepare for Prophet
monthly.columns = ['ds', 'y']
model = Prophet()
model.fit(monthly)

# Forecast next 6 months
future = model.make_future_dataframe(periods=6, freq='M')
forecast = model.predict(future)

# Save forecast
output_file = os.path.join(os.path.dirname(__file__), '../data/forecast_output.csv')
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_csv(output_file, index=False)

# Plot
model.plot(forecast)
plt.show()