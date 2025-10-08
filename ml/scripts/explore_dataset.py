import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('ml/data/DatasetFinal.csv')

# Basic info
print("Data Info:")
print(df.info())
print("\nSample Data:")
print(df.head())

# Check for missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Category-wise spending
category_expense = df.groupby('Category')['Amount'].sum()
category_expense.plot(kind='bar', title='Total Expense by Category')
plt.show()