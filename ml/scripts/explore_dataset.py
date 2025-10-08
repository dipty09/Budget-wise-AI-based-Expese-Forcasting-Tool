# explore_dataset.py

import pandas as pd

# Load the dataset
file_path = "../data/DatasetFinalCSV.csv"
df = pd.read_csv(file_path)

# Basic info
print("✅ Dataset loaded successfully!\n")
print("📊 Shape:", df.shape)
print("\n🔍 Columns:\n", df.columns.tolist())
print("\n🧾 First 5 rows:\n", df.head())
print("\n🧩 Missing values:\n", df.isnull().sum())