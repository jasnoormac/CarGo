import streamlit as st
import subprocess


st.markdown('<h1 class="custom-subtitle">Welcome To Car-Go</h1>', unsafe_allow_html=True)


st.markdown('<h4 class="custom-subtitle">Your one-stop car rental solution</h4stre>', unsafe_allow_html=True)


# Inject CSS for background image
st.markdown(
    """
    <style>
    .stApp {
        background-image: url('https://images8.alphacoders.com/295/295727.jpg');  /* Replace with direct image URL */
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: white;  /* Adjust text color for visibility */
        
    }
    * Add an overlay with reduced opacity */
    .stApp::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(0, 0, 0, 0.5);  /* Adjust the color and opacity */
        z-index: 0;
    }

    /* Ensure content is above the overlay */
    .stApp > div {
        position: relative;
        z-index: 1;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Admin Button
if st.button("Admin"):
    st.write("Opening Admin Login Dashboard...")
    # Run the Admin app file
    subprocess.Popen(["streamlit", "run", "admin.py"])

# User Button
if st.button("User"):
    st.write("Opening User Dashboard...")
    # Run the User app file
    subprocess.Popen(["streamlit", "run", "cust.py"])