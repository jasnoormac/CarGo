import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd
from decimal import Decimal
import datetime


# Database connection
def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="car_rentals"
    )

# Helper functions
def get_data(query, params=None):
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params)
    data = cursor.fetchall()
    conn.close()
    return data

def execute_query(query, params=None):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

# Initialize session state for user selections
if 'user_selections' not in st.session_state:
    st.session_state.user_selections = {
        'car_type': None,
        'vehicle': None,
        'accessories': [],
        'offer': None,
        'discount': None,
        'insurance': None
    }

# Streamlit Layout
st.title("Car-Go")

# Navigation Sidebar
menu = ["Rental Locations", "Car Types", "Vehicle Details", "Insurance", 
         "Car_User","Accessories","Offer Details","Discount","Review and Pay"]
choice = st.sidebar.selectbox("Select Table to Manage", menu)

# Display and manage data for each table
if choice == "Rental Locations":
    st.header("Rental Locations")
    
    # Get unique values for Address, Street Name, and State from the database
    addresses = get_data("SELECT DISTINCT Address FROM Rental_Location")
    street_names = get_data("SELECT DISTINCT Street_Name FROM Rental_Location")
    states = get_data("SELECT DISTINCT State FROM Rental_Location")

    # Extracting the values for dropdown options
    address_options = [address['Address'] for address in addresses]
    street_name_options = [street['Street_Name'] for street in street_names]
    state_options = [state['State'] for state in states]

    # Initialize session state
    if 'address' not in st.session_state:
        st.session_state.address = address_options[0] if address_options else ""
    if 'street_name' not in st.session_state:
        st.session_state.street_name = street_name_options[0] if street_name_options else ""
    if 'state' not in st.session_state:
        st.session_state.state = state_options[0] if state_options else ""

    # Function to update session state
    def update_session_state():
        rental_location = get_data(
            "SELECT Phone, Email, Zip_Code FROM Rental_Location WHERE Address = %s AND Street_Name = %s AND State = %s",
            (st.session_state.address, st.session_state.street_name, st.session_state.state)
        )
        if rental_location:
            st.session_state.phone = rental_location[0]["Phone"]
            st.session_state.email = rental_location[0]["Email"]
            st.session_state.zip_code = rental_location[0]["Zip_Code"]
        else:
            st.session_state.phone = st.session_state.email = st.session_state.zip_code = ""

    # Form to add new rental location
    with st.form("add_rental_location"):
        # Dropdowns populated with data from the database
        st.session_state.address = st.selectbox("Address", address_options, key="address_select")
        st.session_state.street_name = st.selectbox("Street Name", street_name_options, key="street_name_select")
        st.session_state.state = st.selectbox("State", state_options, key="state_select")
        
        # Update session state when form is submitted
        if st.form_submit_button("Update Fields"):
            update_session_state()
        
        # Auto-fill the Phone, Email, and Zip Code fields based on the selection
        phone = st.text_input("Phone", value=st.session_state.get('phone', ''))
        email = st.text_input("Email", value=st.session_state.get('email', ''))
        zip_code = st.text_input("Zip Code", value=st.session_state.get('zip_code', ''))
    # Save rental location details to user selections
    if st.button("Save Rental Location "):
        st.session_state.user_selections['rental_location'] = {
            'address': st.session_state.address,
            'street_name': st.session_state.street_name,
            'state': st.session_state.state,
            'phone': st.session_state.phone,
            'email': st.session_state.email,
            'zip_code': st.session_state.zip_code
        }
        st.success("Rental Location saved!")         
       
    # Update fields when the page loads
    update_session_state()
elif choice == "Car Types":
    st.header("Car Types")

    # Get unique car types from the database
    car_types = get_data("SELECT DISTINCT Car_Type FROM Car_Type")
    car_type_options = [ct['Car_Type'] for ct in car_types]

    # Initialize session state
    if 'car_type' not in st.session_state:
        st.session_state.car_type = car_type_options[0] if car_type_options else ""

    # Function to update session state
    def update_car_type_session_state():
        car_type_data = get_data(
            "SELECT Price_Per_Day, Seating_Capacity FROM Car_Type WHERE Car_Type = %s",
            (st.session_state.car_type,)
        )
        if car_type_data:
            st.session_state.price_per_day = car_type_data[0]["Price_Per_Day"]
            st.session_state.seating_capacity = car_type_data[0]["Seating_Capacity"]
        else:
            st.session_state.price_per_day = st.session_state.seating_capacity = ""

    # Form to add new car type
    with st.form("add_car_type"):
        # Dropdown populated with car types from the database
        st.session_state.car_type = st.selectbox("Car Type", car_type_options, key="car_type_select")
        
        # Update session state when form is submitted
        if st.form_submit_button("Update Fields"):
            update_car_type_session_state()
        
        # Auto-fill the Price Per Day and Seating Capacity fields based on the selection
        price_per_day = st.number_input("Price Per Day", min_value=0.0, value=float(st.session_state.get('price_per_day', 0)))
        seating_capacity = st.number_input("Seating Capacity", min_value=1, step=1, value=int(st.session_state.get('seating_capacity', 1)))
    if st.button("Save Car Type Selection"):
        st.session_state.user_selections['car_type'] = {
            'type': st.session_state.car_type,
            'price_per_day': st.session_state.price_per_day,
            'seating_capacity': st.session_state.seating_capacity
        }
        st.success("Car Type selection saved!")       
        

    # Update fields when the page loads
    update_car_type_session_state()

elif choice == "Vehicle Details":
    st.header("Vehicle Details")

    # Get unique Car Type IDs and Models from the database
    car_types = get_data("SELECT DISTINCT CT.Car_Type_ID, CT.Car_Type FROM Car_Type CT")
    models = get_data("SELECT DISTINCT Model FROM Vehicle_Details")

    car_type_options = [(ct['Car_Type_ID'], ct['Car_Type']) for ct in car_types]
    model_options = [m['Model'] for m in models]

    # Initialize session state
    if 'car_type_id' not in st.session_state:
        st.session_state.car_type_id = car_type_options[0] if car_type_options else (1, "")
    if 'model' not in st.session_state:
        st.session_state.model = model_options[0] if model_options else ""

    # Function to update session state
    def update_vehicle_session_state():
        car_type_data = get_data(
            "SELECT CT.Car_Type, CT.Price_Per_Day, CT.Seating_Capacity FROM Car_Type CT WHERE CT.Car_Type_ID = %s",
            (st.session_state.car_type_id[0],)
        )
        vehicle_data = get_data(
            "SELECT Year, Color, Disable_Friendly FROM Vehicle_Details WHERE Model = %s LIMIT 1",
            (st.session_state.model,)
        )
        
        if car_type_data:
            st.session_state.car_type = car_type_data[0]["Car_Type"]
        if vehicle_data:
            st.session_state.year = vehicle_data[0]["Year"]
            st.session_state.color = vehicle_data[0]["Color"]
            st.session_state.disable_friendly = vehicle_data[0]["Disable_Friendly"]
        else:
            st.session_state.year = 2024
            st.session_state.color = ""
            st.session_state.disable_friendly = False

    # Form to add new vehicle
    with st.form("add_vehicle"):
        # Dropdown for Car Type ID and Model
        st.session_state.car_type_id = st.selectbox("Car Type", car_type_options, format_func=lambda x: f"{x[1]} (ID: {x[0]})", key="car_type_select")
        st.session_state.model = st.selectbox("Model", [""] + model_options, key="model_select")
        
        # Update session state when form is submitted
        if st.form_submit_button("Update Fields"):
            update_vehicle_session_state()
        
        # Auto-fill fields based on the selection
        year = st.number_input("Year", min_value=1900, max_value=2100, value=st.session_state.get('year', 2000))
        color = st.text_input("Color", value=st.session_state.get('color', ''))
        disable_friendly = st.checkbox("Disable Friendly", value=st.session_state.get('disable_friendly', False))
    if st.button("Save Vehicle Selection"):
        st.session_state.user_selections['vehicle'] = {
            'model': st.session_state.model,
            'year': year,
            'color': color,
            'disable_friendly': disable_friendly
        }
        st.success("Vehicle selection saved!")   
       

    # Update fields when the page loads
    update_vehicle_session_state()

#Car_User
elif choice== "Car_User":
    st.header("Car_User")
   
    # Form to add a new Car User
    with st.form("add_car_user"):
        fname = st.text_input("First Name")
        mname = st.text_input("Middle Name")
        lname = st.text_input("Last Name")
        email = st.text_input("Email")
        min_date = datetime.date(1900, 1, 1)
        max_date = datetime.date.today()
        
        dob = st.date_input("Date of Birth", 
                            min_value=min_date,
                            max_value=max_date,
                            value=datetime.date(2000, 1, 1))  # Default to year 2000
        
        license_no = st.text_input("License Number")
        address = st.text_area("Address")
        phone = st.text_input("Phone")

        submit = st.form_submit_button("Add Car User")
        if submit:
            execute_query(
                "INSERT INTO Car_User (FName, MName, LName, Email, DOB, License_No, Address, Phone) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (fname, mname, lname, email, dob, license_no, address, phone)
            )
            # Store user details in session state for review
            st.session_state.user_details = {
                'first_name': fname,
                'middle_name': mname,
                'last_name': lname,
                'email': email,
                'dob': dob,
                'license_no': license_no,
                'address': address,
                'phone': phone
            }
            st.success("Car user added successfully")


elif choice == "Accessories":
    st.header("Accessories")

    # Get unique Accessory Types from the database
    accessory_types = get_data("SELECT DISTINCT Type FROM Accessories")
    accessory_type_options = [a['Type'] for a in accessory_types]

    # Initialize session state
    if 'accessory_type' not in st.session_state:
        st.session_state.accessory_type = accessory_type_options[0] if accessory_type_options else ""

    # Function to update session state
    def update_accessory_session_state():
        accessory_data = get_data(
            "SELECT Accessory_ID, Amount FROM Accessories WHERE Type = %s LIMIT 1",
            (st.session_state.accessory_type,)
        )
        if accessory_data:
            st.session_state.accessory_id = accessory_data[0]["Accessory_ID"]
            st.session_state.amount = float(accessory_data[0]["Amount"])  # Convert to float
        else:
            st.session_state.accessory_id = ""
            st.session_state.amount = 0.0

    # Form to add a new Accessory
    with st.form("add_accessory"):
        # Dropdown for Accessory Type
        st.session_state.accessory_type = st.selectbox("Accessory Type", [""] + accessory_type_options, key="accessory_type_select")
        
        # Update session state when form is submitted
        if st.form_submit_button("Update Fields"):
            update_accessory_session_state()
        
        # Auto-fill fields based on the selection
        accessory_id = st.text_input("Accessory ID", value=st.session_state.get('accessory_id', ''), disabled=True)
        amount = st.number_input("Amount", min_value=0.0, format="%.2f", value=float(st.session_state.get('amount', 0.0)))
    if st.button("Save Accessory Selection"):
        st.session_state.user_selections['accessories'].append({
            'type': st.session_state.accessory_type,
            'amount': amount
        })
        st.success("Accessory selection saved!")  
        

    # Update fields when the page loads
    update_accessory_session_state()

elif choice == "Offer Details":
    st.header("Offer Details")

    # Get unique Promo Codes from the database
    promo_codes = get_data("SELECT DISTINCT Promo_Code FROM Offer_Details")
    promo_code_options = [p['Promo_Code'] for p in promo_codes]

    # Initialize session state
    if 'promo_code' not in st.session_state:
        st.session_state.promo_code = promo_code_options[0] if promo_code_options else ""

    # Function to update session state
    def update_offer_session_state():
        offer_data = get_data(
            "SELECT Description, Status, Is_One_Time FROM Offer_Details WHERE Promo_Code = %s LIMIT 1",
            (st.session_state.promo_code,)
        )
        if offer_data:
            st.session_state.description = offer_data[0]["Description"]
            st.session_state.status = offer_data[0]["Status"]
            st.session_state.is_one_time = offer_data[0]["Is_One_Time"]
        else:
            st.session_state.description = ""
            st.session_state.status = ""
            st.session_state.is_one_time = False

    # Form to add or update an Offer
    with st.form("add_offer"):
        # Dropdown for Promo Code
        st.session_state.promo_code = st.selectbox("Promo Code", [""] + promo_code_options, key="promo_code_select")
        
        # Update session state when form is submitted
        if st.form_submit_button("Update Fields"):
            update_offer_session_state()
        
        # Auto-fill fields based on the selection
        description = st.text_input("Description", value=st.session_state.get('description', ''))
        status = st.text_input("Status", value=st.session_state.get('status', ''))
        is_one_time = st.checkbox("Is One Time", value=st.session_state.get('is_one_time', False))

    if st.button("Save Offer Selection"):
        st.session_state.user_selections['offer'] = {
            'promo_code': st.session_state.promo_code,
            'description': description,
            'status': status,
            'is_one_time': is_one_time
        }
        st.success("Offer selection saved!")
       

    # Update fields when the page loads
    update_offer_session_state()

elif choice == "Discount":
    st.header("Discount")

    # Get unique Promo Codes from the database
    promo_codes = get_data("SELECT DISTINCT Promo_Code FROM Discount")
    promo_code_options = [p['Promo_Code'] for p in promo_codes]

    # Initialize session state
    if 'discount_promo_code' not in st.session_state:
        st.session_state.discount_promo_code = promo_code_options[0] if promo_code_options else ""

    # Function to update session state
    def update_discount_session_state():
        discount_data = get_data(
            "SELECT Discount_ID, Percentage, Discount_Amount FROM Discount WHERE Promo_Code = %s LIMIT 1",
            (st.session_state.discount_promo_code,)
        )
        if discount_data:
            st.session_state.discount_id = discount_data[0]["Discount_ID"]
            st.session_state.percentage = float(discount_data[0]["Percentage"])
            st.session_state.discount_amount = float(discount_data[0]["Discount_Amount"])
        else:
            st.session_state.discount_id = ""
            st.session_state.percentage = 0.0
            st.session_state.discount_amount = 0.0

    # Form to add or update a Discount
    with st.form("add_discount"):
        # Dropdown for Promo Code
        st.session_state.discount_promo_code = st.selectbox("Promo Code", [""] + promo_code_options, key="discount_promo_code_select")
        
        # Update session state when form is submitted
        if st.form_submit_button("Update Fields"):
            update_discount_session_state()
        
        # Auto-fill fields based on the selection
        discount_id = st.text_input("Discount ID", value=st.session_state.get('discount_id', ''), disabled=True)
        percentage = st.number_input("Percentage", min_value=0.0, max_value=100.0, value=float(st.session_state.get('percentage', 0.0)))
        discount_amount = st.number_input("Discount Amount", min_value=0.0, value=float(st.session_state.get('discount_amount', 0.0)))

    if st.button("Save Discount Selection"):
        st.session_state.user_selections['discount'] = {
            'promo_code': st.session_state.discount_promo_code,
            'percentage': percentage,
            'discount_amount': discount_amount
        }
        st.success("Discount selection saved!")
  
        

    # Update fields when the page loads
    update_discount_session_state()

elif choice == "Insurance":
    st.header("Insurance")

    # Get unique Insurance Types from the database
    insurance_types = get_data("SELECT DISTINCT Insurance_Type FROM Insurance")
    insurance_type_options = [i['Insurance_Type'] for i in insurance_types]

    # Initialize session state
    if 'insurance_type' not in st.session_state:
        st.session_state.insurance_type = insurance_type_options[0] if insurance_type_options else ""

    # Function to update session state
    def update_insurance_session_state():
        insurance_data = get_data(
            "SELECT Insurance_ID, Collision_Coverage, Car_Coverage, Medical_Coverage, Insurance_Price FROM Insurance WHERE Insurance_Type = %s LIMIT 1",
            (st.session_state.insurance_type,)
        )
        if insurance_data:
            st.session_state.insurance_id = insurance_data[0]["Insurance_ID"]
            st.session_state.collision_coverage = float(insurance_data[0]["Collision_Coverage"])
            st.session_state.car_coverage = float(insurance_data[0]["Car_Coverage"])
            st.session_state.medical_coverage = float(insurance_data[0]["Medical_Coverage"])
            st.session_state.insurance_price = float(insurance_data[0]["Insurance_Price"])
        else:
            st.session_state.insurance_id = ""
            st.session_state.collision_coverage = 0.0
            st.session_state.car_coverage = 0.0
            st.session_state.medical_coverage = 0.0
            st.session_state.insurance_price = 0.0

    # Form to add or update Insurance
    with st.form("add_insurance"):
        # Dropdown for Insurance Type
        st.session_state.insurance_type = st.selectbox("Insurance Type", [""] + insurance_type_options, key="insurance_type_select")
        
        # Update session state when form is submitted
        if st.form_submit_button("Update Fields"):
            update_insurance_session_state()
        
        # Auto-fill fields based on the selection
    
        collision_coverage = st.number_input("Collision Coverage", min_value=0.0, value=float(st.session_state.get('collision_coverage', 0.0)))
        body_coverage = st.number_input("Car Coverage", min_value=0.0, value=float(st.session_state.get('car_coverage', 0.0)))
        medical_coverage = st.number_input("Medical Coverage", min_value=0.0, value=float(st.session_state.get('medical_coverage', 0.0)))
        insurance_price = st.number_input("Insurance Price", min_value=0.0, value=float(st.session_state.get('insurance_price', 0.0)))
    
    if st.button("Save Insurance Selection"):
        st.session_state.user_selections['insurance'] = {
            'type': st.session_state.insurance_type,
            'collision_coverage': collision_coverage,
            'car_coverage': body_coverage,
            'medical_coverage': medical_coverage,
            'insurance_price': insurance_price
        }
        st.success("Insurance selection saved!")
       
       

    # Update fields when the page loads
    update_insurance_session_state()

elif choice == "Review and Pay":
    st.header("Review Your Selections")
    
    total_amount = Decimal('0.00')
    # Rental Location
    if 'rental_location' in st.session_state.user_selections:
        st.subheader("Rental Location")
        rental_details = st.session_state.user_selections['rental_location']
        st.text_input("Address", value=rental_details['address'], disabled=True, key="rental_address")
        st.text_input("Street Name", value=rental_details['street_name'], disabled=True, key="rental_street")
        st.text_input("State", value=rental_details['state'], disabled=True, key="rental_state")
        st.text_input("Phone", value=rental_details['phone'], disabled=True, key="rental_phone")
        st.text_input("Email", value=rental_details['email'], disabled=True, key="rental_email")
        st.text_input("Zip Code", value=rental_details['zip_code'], disabled=True, key="rental_zip")
    
    if 'car_user' in st.session_state.user_selections:
        st.subheader("Car User Details")
        user_details = st.session_state.user_selections['car_user']
        st.text_input("First Name", value=user_details['first_name'], disabled=True, key="user_fname")
        st.text_input("Middle Name", value=user_details['middle_name'], disabled=True, key="user_mname")
        st.text_input("Last Name", value=user_details['last_name'], disabled=True, key="user_lname")
        st.text_input("Email", value=user_details['email'], disabled=True, key="user_email")
        st.text_input("Date of Birth", value=str(user_details['dob']), disabled=True, key="user_dob")
        st.text_input("License Number", value=user_details['license_no'], disabled=True, key="user_license")
        st.text_area("Address", value=user_details['address'], disabled=True, key="user_address")
        st.text_input("Phone", value=user_details['phone'], disabled=True, key="user_phone")
        
    # Car Type
    if st.session_state.user_selections['car_type']:
        st.subheader("Car Type")
        st.text_input("Type", value=st.session_state.user_selections['car_type']['type'], disabled=True, key="car_type_type")
        st.text_input("Price per Day", value=f"${st.session_state.user_selections['car_type']['price_per_day']:.2f}", disabled=True, key="car_type_price")
        st.text_input("Seating Capacity", value=st.session_state.user_selections['car_type']['seating_capacity'], disabled=True, key="car_type_capacity")
        total_amount += Decimal(str(st.session_state.user_selections['car_type']['price_per_day']))
    #Car_user
    if 'car_user_details' in st.session_state:
        st.subheader("Review Car User Details")
        user_details = st.session_state.car_user_details
    
    # Displaying values in text label boxes (using text inputs for display)
        st.text_input("User ID", value=str(user_details['id']), disabled=True)
        st.text_input("First Name", value=user_details['first_name'], disabled=True)
        st.text_input("Middle Name", value=user_details['middle_name'], disabled=True)
        st.text_input("Last Name", value=user_details['last_name'], disabled=True)
        st.text_input("Email", value=user_details['email'], disabled=True)
        st.text_input("Date of Birth", value=str(user_details['dob']), disabled=True)
        st.text_input("License Number", value=user_details['license_no'], disabled=True)
        st.text_area("Address", value=user_details['address'], disabled=True)
        st.text_input("Phone", value=user_details['phone'], disabled=True)
    # Vehicle
    if st.session_state.user_selections.get('vehicle'):
        st.subheader("Vehicle Details")
        st.text_input("Model", value=st.session_state.user_selections['vehicle'].get('model', ''), disabled=True, key="vehicle_model")
        st.text_input("Year", value=st.session_state.user_selections['vehicle'].get('year', ''), disabled=True, key="vehicle_year")
        st.text_input("Color", value=st.session_state.user_selections['vehicle'].get('color', ''), disabled=True, key="vehicle_color")
        
    # Accessories
    if st.session_state.user_selections['accessories']:
        st.subheader("Accessories")
        for idx, acc in enumerate(st.session_state.user_selections['accessories'], 1):
            st.text_input(f"Accessory {idx}", value=f"{acc['type']} - ${acc['amount']:.2f}", disabled=True, key=f"accessory_{idx}")
            total_amount += Decimal(str(acc['amount']))

    # Offer
    if st.session_state.user_selections['offer']:
        st.subheader("Offer Applied")
        st.text_input("Promo Code", value=st.session_state.user_selections['offer']['promo_code'], disabled=True, key="offer_promo_code")
        st.text_input("Description", value=st.session_state.user_selections['offer']['description'], disabled=True, key="offer_description")

    # Discount
    if st.session_state.user_selections['discount']:
        st.subheader("Discount")
        st.text_input("Promo Code", value=st.session_state.user_selections['discount']['promo_code'], disabled=True, key="discount_promo_code")
        st.text_input("Percentage", value=f"{st.session_state.user_selections['discount']['percentage']}%", disabled=True, key="discount_percentage")
        st.text_input("Discount Amount", value=f"${st.session_state.user_selections['discount']['discount_amount']:.2f}", disabled=True, key="discount_amount")
        total_amount -= Decimal(str(st.session_state.user_selections['discount']['discount_amount']))

    # Insurance
    if st.session_state.user_selections['insurance']:
        st.subheader("Insurance")
        st.text_input("Type", value=st.session_state.user_selections['insurance']['type'], disabled=True, key="insurance_type")
        st.text_input("Collision Coverage", value=f"${st.session_state.user_selections['insurance']['collision_coverage']:.2f}", disabled=True, key="insurance_collision")
        st.text_input("Car Coverage", value=f"${st.session_state.user_selections['insurance']['car_coverage']:.2f}", disabled=True, key="insurance_car")
        st.text_input("Medical Coverage", value=f"${st.session_state.user_selections['insurance']['medical_coverage']:.2f}", disabled=True, key="insurance_medical")
        st.text_input("Insurance Price", value=f"${st.session_state.user_selections['insurance']['insurance_price']:.2f}", disabled=True, key="insurance_price")
        total_amount += Decimal(str(st.session_state.user_selections['insurance']['insurance_price']))

    st.subheader("Total Amount")
    st.text_input("Total", value=f"${total_amount:.2f}", disabled=True, key="total_amount")
    
    if st.button("Proceed to Payment", key="proceed_to_payment"):
        st.session_state.payment_stage = True

    if 'payment_stage' in st.session_state and st.session_state.payment_stage:
        st.header("Payment")
        st.write(f"Total Amount: ${total_amount:.2f}")
        
        payment_method = st.selectbox("Select Payment Method", ["Credit Card", "Debit Card", "PayPal"], key="payment_method")
        card_number = st.text_input("Card Number", key="card_number")
        expiry_date = st.text_input("Expiry Date (MM/YY)", key="expiry_date")
        cvv = st.text_input("CVV", type="password", key="cvv")
        
        if st.button("Make Payment", key="make_payment"):
    # Here you would typically integrate with a payment gateway
    # For this example, we'll just simulate a successful payment
    
            try:
        # Get the User_ID (you might need to implement user authentication)
                user_id = 1  # Replace this with the actual User_ID or implement user authentication

        # Get the Rental_Location_ID (you might need to add this to your user selections)
                rental_location_id = 1  # Replace this with the actual Rental_Location_ID

        # Get the Insurance Amount and ID
                insurance_amount = Decimal('0.00')
                insurance_id = None
                if st.session_state.user_selections.get('insurance'):
                    insurance_amount = Decimal(str(st.session_state.user_selections['insurance'].get('insurance_price', 0)))
                    insurance_id = st.session_state.user_selections['insurance'].get('id')

        # Get the Accessory ID
                accessory_id = None
                if st.session_state.user_selections.get('accessories'):
            # Assuming only one accessory for simplicity. Modify if multiple accessories are allowed.
                    accessory_id = st.session_state.user_selections['accessories'][0].get('id')

        # Get the Discount ID
                discount_id = None
                if st.session_state.user_selections.get('discount'):
                    discount_id = st.session_state.user_selections['discount'].get('id')

        # Get the Car Type ID
                car_type_id = None
                if st.session_state.user_selections.get('car_type'):
                    car_type_id = st.session_state.user_selections['car_type'].get('id')

        # Insert the reservation into the database
                execute_query(
                    """
                    INSERT INTO reservation 
                    (User_ID, Rental_Location_ID, Tot_Amount, Insurance_Amount, Status, Accessory_ID, Insurance_ID, Discount_ID, Car_Type_ID)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (user_id, rental_location_id, float(total_amount), float(insurance_amount), "Confirmed", accessory_id, insurance_id, discount_id, car_type_id)
                )

                st.success("Payment successful and reservation saved!")
        
        # Clear the user selections after successful payment
                st.session_state.user_selections = {
                    'car_type': None,
                    'vehicle': None,
                    'accessories': [],
                    'offer': None,
                    'discount': None,
                    'insurance': None
                }
                st.session_state.payment_stage = False
            except Exception as e:
                st.error(f"An error occurred while saving the reservation: {str(e)}")