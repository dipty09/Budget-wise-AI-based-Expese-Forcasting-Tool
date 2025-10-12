Milestone 1 Documentation: Dataset Acquisition & Frontend Setup

Project: BudgetWise AI-Based Expense Forecasting Tool
Milestone: 1 – Dataset Acquisition and Frontend Initialization
1. Objective

The primary goal of Milestone 1 is to establish the foundation for the project by:

Acquiring a real-world or realistic financial dataset.

Cleaning and preprocessing the dataset to make it suitable for AI/ML modeling.

Setting up the initial Streamlit frontend for visualizing expenses and trends.
2. Dataset Details

Source: Kaggle or other public financial datasets.
File Name: budgetwise_finance_dataset.csv

Key Features:

Feature Name	Description

date	Transaction date
amount	Transaction amount
category	Expense category (e.g., Food, Travel, Rent)
description	Transaction description (optional)

Purpose: The dataset will be used for data cleaning, analysis, and forecasting in future milestones.
3. Data Cleaning and Preprocessing

Script: ml/scripts/explore_dataset.py

Steps Performed:

1. Remove Missing Values

df = df.dropna(subset=['date', 'amount'])

2. Fill Missing Categories
df['category'] = df['category'].fillna('Uncategorized')

3. Convert Amount Column to Numeric
df['amount'] = pd.to_numeric(df['amount'], errors='coerce')

4. Remove Outliers

upper_limit = df['amount'].quantile(0.99)
df = df[df['amount'] < upper_limit]

5. Save Cleaned Data
df.to_csv('ml/data/cleaned_expense_data.csv', index=False)

Outcome: A clean and consistent dataset ready for analysis and model integration.
4. Frontend Setup

Framework: Streamlit (Python Web Dashboard)
File: frontend/app.py

Purpose:

Visualize the dataset for initial exploration.

Display total spending per category and basic trends.

Confirm integration with the cleaned dataset.


Key Features Implemented:

Dataset preview using st.dataframe().

Bar chart visualization of total expenses per category.

Interactive dashboard layout.

5. Folder Structure

budget-wise-ai-based-expese-forcasting-tool/
│
├── ml/
│   ├── data/
│   │   ├── budgetwise_finance_dataset.csv
│   │   └── cleaned_expense_data.csv
│   └── scripts/
│       └── explore_dataset.py
│
├── frontend/
│   └── app.py
│
├── documentation.md
└── requirements.txt

6. Outcome of Milestone 1

✅ Acquired a real-world expense dataset.

✅ Performed data cleaning and preprocessing.

✅ Generated a cleaned CSV file for ML modeling.

✅ Set up an initial Streamlit dashboard for data visualization.

✅ Documented all steps and folder organization for reproducibility.