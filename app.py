import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

st.title("HR Dashboard program")

#Tab Bar to swap between functions
Tab_Dashboard, Tab_Add, Tab_Update = st.tabs(["HR Dashboard","Add New Employee","Update state of Employee"])

#connect SQL to program
def get_connection():
    return sqlite3.connect("mydb.db")

#Load data to program
def load_employees():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM Employees", conn)
    return df

#Insert new data in database only in  EmployeeNumber, Department, MonthlyIncome
def add_employee(employee_id, department, new_role, income):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO employees (EmployeeNumber, Department,JobRole, MonthlyIncome) VALUES (?, ?, ?, ?)",
              (employee_id, department,new_role, income))
    conn.commit()
    conn.close() 

#Chack the data inserted if exist by ID Employee 
def employee_exists(employee_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT EmployeeNumber FROM employees WHERE EmployeeNumber = ?", (employee_id,))
    exists = c.fetchone() is not None
    conn.close() 
    return exists

#update the information in the database by ID of Employee
def update_employee(emp_id, income):
    try:
        with sqlite3.connect('mydb.db') as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE employees SET MonthlyIncome = ? WHERE EmployeeNumber = ?", 
                (float(income), int(emp_id))
            )
            conn.commit()
            if cursor.rowcount == 0:
                return False, "No employee found with that ID"
            return True, "Update successful"
    except Exception as e:
        return False, str(e)

def get_departments():
    with sqlite3.connect('mydb.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT Department FROM employees")
        rows = cursor.fetchall()
    return [row[0] for row in rows]

def get_job_roles():
    with sqlite3.connect('mydb.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT JobRole FROM employees")
        rows = cursor.fetchall()
    return [row[0] for row in rows]


def next_employee_id():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT MAX(EmployeeNumber) FROM employees")
    max_id = c.fetchone()[0]
    conn.close()
    
    if max_id is None:
        return 1
    else:
        return max_id + 1
    

df = load_employees()



with Tab_Dashboard:

    
    department_filter = st.selectbox("Filter by Department:", options=["All"] + sorted(df["Department"].unique().tolist()))
    filtered_df = df if department_filter == "All" else df[df["Department"] == department_filter]


    fig_bar = px.bar(filtered_df, x="Department", y="MonthlyIncome", color="Department", title="Employee Income by Department")
    st.plotly_chart(fig_bar)

    fig_pie = px.pie(df, names="Department", title="Employee Count by Department")
    st.plotly_chart(fig_pie)

    fig_H2 = px.histogram(df, y="Education", color="Department", barmode="group",title="Percentage of Education Levels by Department")
    st.plotly_chart(fig_H2)

    fig_histogram = px.histogram(df,x="Gender", color="Department", barmode="group", title="Gender by Department")
    st.plotly_chart(fig_histogram)

    st.subheader("Employee Table")
    st.dataframe(filtered_df)


    with Tab_Add:
        with st.form("add_employee_form"):
            st.header("Add a New Employee")
            next_id = next_employee_id()
            new_employee_ID = st.number_input("Employee Number", min_value=1, value=next_id, format="%d")
            Department = get_departments
            new_dept = st.selectbox("Departments", options= get_departments(), key="Department")
            Jobrole = get_job_roles
            new_role = st.selectbox("Job Role", options= get_job_roles(), key="Job Role select")
            new_income = st.number_input("Monthly Income", min_value=0, step=1000, format="%d")
            submitted = st.form_submit_button("Add Employee")

            if submitted:
                if employee_exists(new_employee_ID):
                    st.error("This Employee ID already exists. Please use a unique ID.")
                elif not new_dept or not new_role or not new_employee_ID or not new_income:
                    st.warning("Please fill in all the details.")
                else:
                    add_employee(new_employee_ID, new_dept, new_role, new_income)
                    st.success("Successfully added employee to the database!")
                    st.session_state['df'] = load_employees() 
                    st.rerun()


    with Tab_Update:
        st.title("Update Employee Monthly Income")

        emp_id = st.text_input("Employee ID")
        income = st.text_input("New Monthly Income")

        if st.button("Check Employee Exists"):
            if emp_id.isdigit():
                if employee_exists(emp_id):
                    st.success(f"Employee {emp_id} found!")
                else:
                    st.error(f"Employee {emp_id} not found.")
            else:
                st.error("Employee ID must be a number.")

        if st.button("Update Income"):
            if not emp_id.isdigit():
                st.error("Employee ID must be a number")
            else:
                try:
                    float(income)
                    success, msg = update_employee(emp_id, income)
                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)
                except ValueError:
                    st.error("Monthly Income must be a number")