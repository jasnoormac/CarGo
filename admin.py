import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd
import subprocess
import os  # for environment variables

# Database connection
def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",  # Consider using os.getenv("DB_PASSWORD") for security
        database="car_rentals"
    )

# Helper functions
def get_data(query):
    try:
        conn = create_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        data = cursor.fetchall()
        return pd.DataFrame(data)
    except Error as e:
        st.error(f"Database Error: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def execute_query(query, params=None):
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
    except Error as e:
        st.error(f"Error executing query: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def authenticate_admin(admin_id, password):
    try:
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)
        # Querying based on `admin_id` and `password` columns directly
        query = "SELECT * FROM login WHERE admin_id = %s AND password = %s"
        cursor.execute(query, (admin_id, password))
        result = cursor.fetchone()
        return result is not None
    except Error as e:
        st.error(f"Error: {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def admin_login():
    st.title("Admin Login")

    # Create a form for admin login
    with st.form("admin_login_form"):
        admin_id = st.text_input("Admin ID")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")

    if submit_button:
        if authenticate_admin(admin_id, password):
            st.success("Login successful!")
            st.write("Opening Admin Dashboard...")
            # Run the main admin application (app.py)
            subprocess.Popen(["streamlit", "run", "app.py"])
        else:
            st.error("Invalid credentials. Please try again.")

# Run the login function
if __name__ == "__main__":
    admin_login()
