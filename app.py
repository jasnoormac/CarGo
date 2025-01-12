import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd

# Database connection
def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="car_rentals"
    )

# Helper functions
def get_data(query):
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return pd.DataFrame(data)

def execute_query(query, params=None):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

# Streamlit Layout
st.title("Admin")

# Navigation Sidebar
menu = ["Rental Locations", "Car Types", "Vehicle Details", "Insurance",
           "Accessories", "Offer Details", "Discount",]
choice = st.sidebar.selectbox("Select Table to Manage", menu)

# Display and manage data for each table
if choice == "Rental Locations":
    st.header("Rental Locations")
    # View data
   
    # Form to add new rental location
    with st.form("add_rental_location"):
        phone = st.text_input("Phone")
        email = st.text_input("Email")
        address = st.text_input("Address")
        street_name = st.text_input("Street Name")
        state = st.text_input("State")
        zip_code = st.text_input("Zip Code")
        submit = st.form_submit_button("Add Rental Location")
        if submit:
            execute_query(
                "INSERT INTO Rental_Location (Phone, Email, Address, Street_Name, State, Zip_Code) VALUES (%s, %s, %s, %s, %s, %s)",
                (phone, email, address, street_name, state, zip_code)
            )
            st.success("Rental location added successfully")

# Repeat similar structures for other tables
elif choice == "Car Types":
    st.header("Car Types")
    
    # Add form for Car Types
    with st.form("add_car_type"):
        car_type = st.text_input("Car Type")
        price_per_day = st.number_input("Price Per Day", min_value=0.0)
        seating_capacity = st.number_input("Seating Capacity", min_value=1, step=1)
        submit = st.form_submit_button("Add Car Type")
        if submit:
            execute_query(
                "INSERT INTO Car_Type (Car_Type, Price_Per_Day, Seating_Capacity) VALUES (%s, %s, %s)",
                (car_type, price_per_day, seating_capacity)
            )
            st.success("Car type added successfully")

# Example for Reservations table with additional fields and validation
elif choice == "Reservations":
    st.header("Reservations")
   

    with st.form("add_reservation"):
        user_id = st.number_input("User ID", min_value=1, step=1)
        vin = st.text_input("VIN")
        rental_location_id = st.number_input("Rental Location ID", min_value=1, step=1)
        drop_location_id = st.number_input("Drop Location ID", min_value=1, step=1)
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
        rental_amount = st.number_input("Rental Amount", min_value=0.0)
        submit = st.form_submit_button("Add Reservation")
        if submit:
            execute_query(
                "INSERT INTO Reservation (User_ID, VIN, Rental_Location_ID, Drop_Location_ID, Start_Date, End_Date, Rental_Amount) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (user_id, vin, rental_location_id, drop_location_id, start_date, end_date, rental_amount)
            )
            st.success("Reservation added successfully")
# Vehicle Details
elif choice == "Vehicle Details":
    st.header("Vehicle Details")
   
    with st.form("add_vehicle"):
        vin = st.text_input("VIN")
        reg_no = st.text_input("Registration Number")
        model = st.text_input("Model")
        year = st.number_input("Year", min_value=1900, step=1)
        color = st.text_input("Color")
        disable_friendly = st.checkbox("Disable Friendly")
        car_type_id = st.number_input("Car Type ID", min_value=1, step=1)
        submit = st.form_submit_button("Add Vehicle")
        if submit:
            execute_query(
                "INSERT INTO Vehicle_Details (VIN, Reg_No, Model, Year, Color, Disable_Friendly, Car_Type_ID) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (vin, reg_no, model, year, color, disable_friendly, car_type_id)
            )
            st.success("Vehicle added successfully")

# Insurance
elif choice == "Insurance":
    st.header("Insurance")
    
    with st.form("add_insurance"):
        insurance_type = st.text_input("Insurance Type")
        collision_coverage = st.number_input("Collision Coverage", min_value=0.0)
        body_coverage = st.number_input("Body Coverage", min_value=0.0)
        medical_coverage = st.number_input("Medical Coverage", min_value=0.0)
        insurance_price = st.number_input("Insurance Price", min_value=0.0)
        submit = st.form_submit_button("Add Insurance")
        if submit:
            execute_query(
                "INSERT INTO Insurance (Insurance_Type, Collision_Coverage, Body_Coverage, Medical_Coverage, Insurance_Price) VALUES (%s, %s, %s, %s, %s)",
                (insurance_type, collision_coverage, body_coverage, medical_coverage, insurance_price)
            )
            st.success("Insurance added successfully")

# Insurance Coverage
elif choice == "Insurance Coverage":
    st.header("Insurance Coverage")
   
    with st.form("add_insurance_coverage"):
        car_type_id = st.number_input("Car Type ID", min_value=1, step=1)
        insurance_id = st.number_input("Insurance ID", min_value=1, step=1)
        submit = st.form_submit_button("Add Insurance Coverage")
        if submit:
            execute_query(
                "INSERT INTO Insurance_Coverage (Car_Type_ID, Insurance_ID) VALUES (%s, %s)",
                (car_type_id, insurance_id)
            )
            st.success("Insurance coverage added successfully")


# Offer Details
elif choice == "Offer Details":
    st.header("Offer Details")
   
    with st.form("add_offer"):
        promo_code = st.text_input("Promo Code")
        description = st.text_input("Description")
        status = st.text_input("Status")
        is_one_time = st.checkbox("Is One Time")
        submit = st.form_submit_button("Add Offer")
        if submit:
            execute_query(
                "INSERT INTO Offer_Details (Promo_Code, Description, Status, Is_One_Time) VALUES (%s, %s, %s, %s)",
                (promo_code, description, status, is_one_time)
            )
            st.success("Offer added successfully")

# Discount
elif choice == "Discount":
    st.header("Discount")
   
    with st.form("add_discount"):
        promo_code = st.text_input("Promo Code")
        percentage = st.number_input("Percentage", min_value=0.0, max_value=100.0)
        discount_amount = st.number_input("Discount Amount", min_value=0.0)
        submit = st.form_submit_button("Add Discount")
        if submit:
            execute_query(
                "INSERT INTO Discount (Promo_Code, Percentage, Discount_Amount) VALUES (%s, %s, %s)",
                (promo_code, percentage, discount_amount)
            )
            st.success("Discount added successfully")

#Car_User
elif choice== "Car_User":
    st.header("Car_User")
   
    # Form to add a new Car User
    with st.form("add_car_user"):
        fname = st.text_input("First Name")
        mname = st.text_input("Middle Name")
        lname = st.text_input("Last Name")
        email = st.text_input("Email")
        dob = st.date_input("Date of Birth")
        license_no = st.text_input("License Number")
        address = st.text_area("Address")
        phone = st.text_input("Phone")

        submit = st.form_submit_button("Add Car User")
        if submit:
            execute_query(
                "INSERT INTO Car_User (FName, MName, LName, Email, DOB, License_No, Address, Phone) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (fname, mname, lname, email, dob, license_no, address, phone)
            )
            st.success("Car user added successfully")

# Accessories
elif choice == "Accessories":
    st.header("Accessories")
    
    
    with st.form("add_accessory"):
        accessory_type = st.text_input("Accessory Type")
        amount = st.number_input("Amount", min_value=0.0)
        submit = st.form_submit_button("Add Accessory")
        
        if submit:
            execute_query(
                "INSERT INTO Accessories (Type, Amount) VALUES (%s, %s)",
                (accessory_type, amount)
            )
            st.success("Accessory added successfully")
# Continue similar patterns for other tables

# Other forms and interaction for remaining tables can follow the same pattern