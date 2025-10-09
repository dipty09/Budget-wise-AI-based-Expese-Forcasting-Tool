import pandas as pd
import matplotlib.pyplot as plt

# Load forecast output
forecast = pd.read_csv('../data/forecast_output.csv')

# Display top 5 records
print("Forecast Preview:")
print(forecast.head())

# Visualize the forecast results
plt.figure(figsize=(10, 6))
plt.plot(forecast['ds'], forecast['yhat'], label='Predicted Value', color='blue')
plt.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], color='lightblue', alpha=0.4)
plt.title('AI-Based Expense Forecast')
plt.xlabel('Date')
plt.ylabel('Forecasted Amount')
plt.legend()
plt.show()
plt.savefig('../data/forecast_plot.png')