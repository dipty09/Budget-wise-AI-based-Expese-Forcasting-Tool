### Milestone 1: Weeks 1–2 — User Authentication & Basic Transaction Input

 ### 1. Objective

The goal of Milestone 1 is to build the foundation of the BudgetWise AI-Based Expense Forecasting Tool by implementing user authentication and basic transaction management modules.
This phase focuses on enabling secure access, personalized profiles, and manual data entry for financial records.


---

### 2. High-Level Requirements

a. User Registration

Implement a secure registration system using email and password.

Ensure data is stored securely in the backend database (e.g., MongoDB or MySQL).

Apply password hashing (using libraries like bcrypt) to protect user credentials.

Validate unique email entries and enforce strong password rules.



---

## b. Login System

Develop a robust authentication mechanism using JWT (JSON Web Token) for secure session management.

Generate a token upon successful login and validate it for all protected routes.

Implement error handling for invalid credentials or expired tokens.



---

## c. Profile Management

Allow users to manage and update their personal profile (name, email, etc.).

Display user-specific financial summaries after login.

Maintain individual user contexts for personalized data storage.



---

## d. Manual Transaction Input

Design a Streamlit-based frontend for simple manual transaction entry.

Enable users to input:

Date

Amount

Category (Income / Expense)

Description (optional)


Store each entry in the backend database for future analytics.

Provide confirmation upon successful submission.



---

### 3. Technology Stack

Component	Technology Used

Frontend	Streamlit (Python-based UI)
Backend	Flask / Node.js (API-based architecture)
Database	MongoDB / MySQL
Authentication	JWT (JSON Web Token)
Password Security	bcrypt
Environment	Python 3.11 with virtual environment setup



---

 ### 4. Folder Structure (Milestone 1)

budgetwise-expense-forecasting-tool/
│
├── backend/
│   ├── app.py
│   ├── routes/
│   │   ├── auth_routes.py
│   │   └── transaction_routes.py
│   └── models/
│       └── user_model.py
│
├── frontend/
│   └── app.py
│
├── ml/
│   ├── data/
│   └── scripts/
│
└── requirements.txt


---

### 5. Expected Output

a. User Registration Page

Interface for new users to register securely.

Validation for email and password.

Confirmation message after successful signup.


b. Login Page

User can log in using registered credentials.

Invalid credentials trigger error messages.

After successful login, JWT token generated.


c. Transaction Input Form

User can enter new transactions manually.

Input fields: Date, Amount, Category, Description.

Saved transactions displayed in a table below the form.



---

### 6. Outcome

✅ Implemented a secure authentication system (Registration + Login).
✅ Created user-specific profile management functionality.
✅ Developed a manual transaction input interface using Streamlit.
✅ Ensured data storage consistency and validation for future ML integration.
✅ Established the core foundation for financial tracking and expense forecasting.
### Milestone 2: Weeks 3-4 Module 2: Transaction Categorization & Basic Reporting

## High-Level Requirements

Automated Categorization
Implemented a rule-based or keyword-based system to categorize transactions into categories such as Groceries, Rent, Transport, Utilities, and Entertainment. Users can manually override the category if needed.

Spending Summary Reports
Reports are generated using Pandas to summarize total spending per category, monthly spending trends, and Income vs. Expense analysis. The data can be exported as CSV or visualized in charts.

Dashboard & Visualizations
Streamlit displays recent transactions and summaries in an interactive dashboard. Visualizations include pie charts for category-wise spending and bar charts for monthly trends. Users can filter data using interactive Streamlit widgets.

## Example Output Screenshots

Categorized Transactions Table

Pie Chart: Spending by Category

Bar Chart: Monthly Spending

Streamlit Dashboard