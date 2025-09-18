📊 HR Dashboard Program

A Streamlit-based web application to manage and visualize employee data using an SQLite database. It allows HR professionals to:

📈 View insightful employee analytics and dashboards

➕ Add new employee records

✏️ Update existing employee income

🚀 Features
1. HR Dashboard Tab
Interactive charts powered by Plotly:
Employee income by department
Employee count by department (pie chart)
Education levels per department
Gender distribution across departments
Filter data by department
View employee data in a structured table

2. Add New Employee Tab
Auto-suggests the next available employee ID
Select department and job role from existing database values
Input monthly income
Prevents duplicate Employee IDs

3. Update Employee Tab
Check if an employee exists by ID
Update their monthly income

🗂️ Project Structure
├── app.py               # Main Streamlit application
├── mydb.db              # SQLite database file
├── README.md            # Project documentation
├── T-1-HR               # Question and answer File 

🧰 Tech Stack
Python
- Streamlit for UI
- SQLite for database
- Pandas for data manipulation
- Plotly Express for data visualization

⚙️ Installation & Setup

Clone the repository

git clone https://github.com/your-username/hr-dashboard.git
cd hr-dashboard


Install dependencies
Make sure you’re using Python 3.10.

pip install streamlit pandas plotly


Set up the database
Ensure mydb.db exists and includes a table named employees with at least the following columns:

CREATE TABLE employees (
    EmployeeNumber INTEGER PRIMARY KEY,
    Department TEXT,
    JobRole TEXT,
    MonthlyIncome REAL,
    Gender TEXT,
    Education TEXT
);


⚠️ Add some sample data before running the app for the first time.

Run the app

streamlit run app.py

📝 Notes

The app does not support deleting records.

Assumes departments and job roles are already present in the database to populate dropdowns.

Employee IDs must be unique integers.

📸 Sample Screenshots (Optional)

You can add screenshots of:

The dashboard with graphs

Add employee form

Update employee form

📬 Feedback or Contributions

Feel free to fork this project or open issues for bugs and improvements.

📄 License

This project is licensed under the MIT License.