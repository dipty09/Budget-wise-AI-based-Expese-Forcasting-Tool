import pandas as pd
import numpy as np
import os


csv_path = r"D:\Budget Expense_tool\budget-wise-ai-based-expese-forcasting-tool\ml\data\budgetwise_finance_dataset.csv"
df = pd.read_csv(csv_path)


print("Columns in dataset:", df.columns)

df.columns = df.columns.str.strip().str.lower()


df = df.dropna(subset=['date', 'amount'])
df['category'] = df['category'].fillna('uncategorized')


df['amount'] = df['amount'].replace({',': '', '₹': '', '$': ''}, regex=True)
df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
df = df.dropna(subset=['amount'])

df['date'] = pd.to_datetime(df['date'], errors='coerce')
df = df.dropna(subset=['date'])


df['month'] = df['date'].dt.month
df['weekday'] = df['date'].dt.day_name()
df['year'] = df['date'].dt.year


print("Dataset info:")
print(df.info())

print("\nDataset description:")
print(df.describe())

lower_limit = df['amount'].quantile(0.01)
upper_limit = df['amount'].quantile(0.99)
print(f"\nAmount lower 1% quantile: {lower_limit}")
print(f"Amount upper 99% quantile: {upper_limit}")

print("\nSample cleaned data:")
print(df.head())


output_folder = r"D:\Budget Expense_tool\budget-wise-ai-based-expese-forcasting-tool\ml\data"
os.makedirs(output_folder, exist_ok=True)

cleaned_csv_path = os.path.join(output_folder, "budgetwise_finance_dataset_cleaned.csv")
df.to_csv(cleaned_csv_path, index=False)
print(f"\nCleaned dataset saved to: {cleaned_csv_path}")