import pandas as pd
import matplotlib.pyplot as plt

# Load datasets
df = pd.read_csv('../data/DatasetFinalCSV.csv')
forecast = pd.read_csv('../data/forecast_output.csv')

# Convert Month to datetime (assume all data is 2024)
df['Month_Year'] = pd.to_datetime(df['Month'] + ' 2024', format='%B %Y')
df['Month_Year'] = df['Month_Year'].dt.to_period('M')

forecast['Month_Year'] = pd.to_datetime(forecast['ds']).dt.to_period('M')

# Merge datasets
comparison = pd.merge(df, forecast, on='Month_Year', how='inner')

# Plot
plt.plot(comparison['Month_Year'].astype(str), comparison['yhat'], label='Forecast', linestyle='--')
plt.plot(comparison['Month_Year'].astype(str), comparison['AmountOfProduct'], label='Actual', marker='o')
plt.xlabel('Month')
plt.ylabel('Amount of Product')
plt.title('Actual vs Forecast Comparison')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()