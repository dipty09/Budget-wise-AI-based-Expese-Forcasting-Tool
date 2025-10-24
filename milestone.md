# **Budget Expense Forecasting Tool**

---

 ## 1.**Project Statement:**
Many individuals struggle with managing their personal finances effectively, often finding it difficult to track spending, stick to a budget, and plan for future financial goals. The sheer volume of daily transactions can be overwhelming, making it hard to identify spending patterns or anticipate upcoming expenses. This lack of financial clarity can lead to stress, missed savings opportunities, and difficulty in achieving long-term financial stability. The "Personal Budgeting & Expense Forecaster" project aims to address these challenges by developing an intuitive tool that helps individuals gain control over their finances. By leveraging time-series forecasting on historical transaction data (using simulated or dummy data), the application will enable users to visualize spending patterns, set realistic financial goals, and forecast future expenses and savings, empowering them to make informed financial decisions.
It is a Streamlit-based financial management system that enables users to record, categorize, and visualize their income and expenses. The application provides users with an intuitive dashboard for tracking financial activities through secure authentication, transaction management, and visual analytics.

---
 ## 2.**Outcomes:** 

 - Clear Financial Overview: Provide users with an easy-to-understand dashboard of their income, expenses, and savings.

 - Automated Expense Forecasting: Predict future spending based on historical data, helping users anticipate financial needs.

 - Spending Pattern Identification: Automatically categorize transactions and highlight key spending areas.

 -  Goal-Oriented Planning: Assist users in setting and tracking progress towards financial goals (e.g., saving for a down payment, retirement).

 - Data-Driven Insights: Empower users to identify areas for potential savings and
   improve budgeting habits.

 - User-Friendly Interface: An intuitive platform for inputting transactions, viewing reports, and interacting with forecasts.

---

 ## 3.**Module To be Implemented**  
 ### User Authentication and profile Management:
    
   - Basic user profile for managing financial data and preferences.

 ### Transaction Ingestion & Categorization Module:

   - Interface for users to manually input or upload simulated/dummy transaction data (ee.g., CSV).

   - Automated (or semi-automated, rule-based) categorization of transactions (e.g.. 'Groceries', 'Utilities', 'Transport').

 ### Data Analysis & Reporting Module:

   - Calculate spending summaries per category, month, or custom period.
   - Generate reports on income vs. expenses.

### Forecasting Module:

   - Implement Prophet (Meta's forecasting library) to predict future expenses and income based on historical transaction patterns.

   - Allow users to define financial goals and forecast their achievement.

### Visualization & Dashboard Module:
   - Interactive charts and graphs (using Matplotlib, Seaborn) to visualize spending
---

 ## 4.**Module Representation And Requirements With output ScreenShots:** 


## **Milestone 1: Weeks 1–2**
### **Module 1: User Authentication & Basic Transaction Input**

### **Objective**
To establish a secure user authentication mechanism and develop an interface for users to input and manage their financial transactions effectively.

---

### **High-Level Requirements**

#### **1. User Registration**
- Secure registration using email and password.
- Passwords are encrypted before storage in the database.
- JWT (JSON Web Token) is implemented for secure session management.
- Duplicate registration is prevented via unique email verification.

#### **2. Login System**
- Secure login authentication with JWT-based token generation.
- Session-based user identification to protect restricted routes.
- Proper handling of invalid or expired login attempts.

#### **3. Profile Management**
- Users can view and update profile details (name, email, and password).
- All updates are validated and securely processed.
- Each profile is linked to its user data via a relational user ID.

#### **4. Manual Transaction Input**
- Streamlit interface designed for user-friendly data entry.
- Input fields include:
  - Date  
  - Amount  
  - Description  
  - Type (Income / Expense)
- Data stored securely in the database and linked to the authenticated user.

---

### **Technological Implementation**
- **Frontend:** Streamlit forms and UI components for user interaction.
- **Backend:** Python-based logic with JWT authentication and database operations.
- **Database:** SQLite/MySQL for storing user and transaction data.
- **Security:** Password hashing with bcrypt and session validation using JWT.

---

### **Expected Outputs**
- Successful registration and login via Streamlit interface.
- Transaction input form storing dummy transactions in the database.
- Profile management and user-specific data display.

#### **Sample Output Screenshots**
- User Registration Form  
- Login Page Interface  
- Transaction Input Form  
- Profile Management Screen  

---

## **Milestone 2: Weeks 3–4**
### **Module 2: Transaction Categorization & Basic Reporting**

### **Objective**
To implement automated transaction categorization and visualization through analytical dashboards and summary reports.

---

### **High-Level Requirements**

#### **1. Automated Transaction Categorization**
- Rule-based categorization using keyword matching for identifying transaction types.
- Supported categories include:
  - Groceries  
  - Rent  
  - Transport  
  - Utilities  
  - Entertainment
- Users can manually modify category assignments if needed.
- Descriptions are processed to match relevant categories automatically.

#### **2. Spending Summary Reports**
- Summarization using Pandas to generate:
  - Total spending per category.  
  - Monthly spending reports.  
  - Income vs. Expense analysis.
- Option to export spending summaries as CSV files.
- Integration of financial statistics for quick decision-making.

#### **3. Dashboard & Visualization**
- Streamlit dashboard displays real-time financial insights.
- Visual representation using Matplotlib and Seaborn.
- Charts include:
  - **Pie Chart:** Spending distribution by category.
  - **Bar Chart:** Monthly spending trends.
- Filters and selectors for interactive data exploration.

---

### **Technological Implementation**
- **Frontend:** Streamlit-based dashboard with visual analytics.
- **Backend:** Python logic for transaction categorization and report generation.
- **Database:** SQLite/MySQL for storing categorized transaction records.
- **Visualization Tools:**  
  - Matplotlib for static visual representation.  
  - Seaborn for aesthetically enhanced analytics charts.

---

### **Expected Outputs**
- Categorized transactions displayed in a structured table.
- Streamlit dashboard with:
  - Pie chart visualization for spending by category.  
  - Bar chart for monthly trends.  
  - Recent transactions overview.
- Exportable CSV summary reports for further analysis.

#### **Sample Output Screenshots**
- Categorized Transactions Table  
- Spending Summary Report  
- Pie Chart – Category-wise Spending  
- Bar Chart – Monthly Expense Overview  
- Dashboard Overview  

---

## **Key Achievements (Milestone 1 & 2)**
- Developed a **secure authentication system** using JWT and password hashing.  
- Implemented **user-friendly transaction input** via Streamlit forms.  
- Created **automated categorization logic** for expense classification.  
- Built **interactive dashboards** for financial insights using Matplotlib and Seaborn.  
- Generated **summary reports** for enhanced expense analysis and forecasting.

---


---

