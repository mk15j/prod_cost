import streamlit as st
import pandas as pd
from pymongo import MongoClient
import bcrypt
import os
import time
from dotenv import load_dotenv

# Load MongoDB URI from Streamlit Secrets
MONGO_URI = st.secrets["MONGO_URI"]

if not MONGO_URI:
    st.error("MongoDB connection string not found! Check your Streamlit Secrets.")
    st.stop()

# MongoDB Connection
client = MongoClient(MONGO_URI)
db = client["user_management"]
users_collection = db["users"]
data_collection = db["user_data"]
rate_collection = db["rates_data"]
pack_collection = db["pack_data"]

# Set Streamlit page config
st.set_page_config(page_title="Captain Fresh Trient Orders", layout="wide")

# Session State Initialization
if "page" not in st.session_state:
    st.session_state["page"] = "login"
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
    st.session_state["username"] = ""
    st.session_state["role"] = ""

def navigate(page):
    if st.session_state["page"] != page:
        st.session_state["page"] = page
        st.write(f"Navigating to {page}")  # Debug message
        time.sleep(0.5)  # Prevents flickering
        st.rerun()

def login():
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    col1, col2 = st.columns([1, 1])
    if col1.button("Login", key="login_button"):
        user = users_collection.find_one({"username": username})
        # st.write(f"User found - {user}")  # Debug info

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.session_state["role"] = user["role"]
            st.success("Login successful! Redirecting...")
            time.sleep(1)
            navigate("user_dashboard" if user["role"] == "user" else "admin_dashboard")
        else:
            st.error("Invalid username or password")
    
    if col2.button("Register", key="register_button"):
        navigate("register")

def register():
    st.title("Register Page")
    new_username = st.text_input("Choose a username")
    new_password = st.text_input("Choose a password", type="password")
    role = st.selectbox("Select Role", ["user", "admin"])
    
    col1, col2 = st.columns([1, 1])
    if col1.button("Submit Registration", key="submit_register"):
        if not new_username or not new_password:
            st.error("Username and Password cannot be empty.")
            return

        if users_collection.find_one({"username": new_username}):
            st.error("Username already exists! Try another one.")
        else:
            hashed_pw = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            users_collection.insert_one({"username": new_username, "password": hashed_pw, "role": role})
            st.success("Registration successful! Redirecting to login...")
            time.sleep(1)
            navigate("login")
    
    if col2.button("Back to Login", key="back_to_login"):
        navigate("login")
######################
# Admin CSV Upload Function
def admin_upload_csv():
    st.title("Admin: Upload Filleting Rates Data File")

    uploaded_file = st.file_uploader("Upload Rates File", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        # Validate required columns
        required_columns = {"product", "trim_type", "rm_spec", "rate_per_kg"}
        if not required_columns.issubset(df.columns):
            st.error(f"Filleting file must contain columns: {', '.join(required_columns)}")
            return

        # Add admin username for tracking
        username = st.session_state.get("username", "admin")

        # Convert DataFrame to MongoDB format
        data_list = df.to_dict(orient="records")
        for item in data_list:
            item["username"] = username  # Track uploader

        # Insert data into MongoDB
        rate_collection.insert_many(data_list)
        st.success("Filleting Rates data uploaded successfully!")


######################################################################

# Admin Pack CSV Upload Function
def pack_upload_csv():
    st.title("Admin: Upload Packaging Rates Data File")

    uploaded_file = st.file_uploader("Upload Rates File", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        # Validate required columns
        required_columns = {"prod_type","product", "box_qty", "pack", "transport_mode", "packaging_rate"}
        if not required_columns.issubset(df.columns):
            st.error(f"Packaging file must contain columns: {', '.join(required_columns)}")
            return

        # Add admin username for tracking
        username = st.session_state.get("username", "admin")

        # Convert DataFrame to MongoDB format
        data_list = df.to_dict(orient="records")
        for item in data_list:
            item["username"] = username  # Track uploader

        # Insert data into MongoDB
        pack_collection.insert_many(data_list)
        st.success("CSV Packaging Rates data uploaded successfully!")

# Admin Dashboard
def admin_dashboard():
    st.title("Admin Dashboard")
    st.write(f"Welcome, {st.session_state['username']}!")

    st.sidebar.subheader("Rates Links")

    if st.sidebar.button("Filleting Rates"):
        admin_upload_csv()
        # navigate("admin_upload_csv")
    elif st.sidebar.button("Packaging Rates"):
        pack_upload_csv()
        # navigate("pack_upload_csv")
    
    st.subheader("Enquiries Details")
    users = list(data_collection.find({}, {"_id": 0}))
    if users:
        st.table(users)
    else:
        st.write("No data available.")



# User Dashboard
def user_dashboard():
    st.title("User Dashboard")
    # st.write(f"Welcome, {st.session_state['username']}!")

    st.sidebar.subheader("User Links")
    
     # Create two columns for Order Form and Order Details
    col1, col2 = st.columns([2, 1], gap="large")  # Increased gap between sections
    
    with col1:
    #   st.subheader("Enquiries Details")
      user_form()
    
    with col2:
        st.subheader("Compulsory Charges")
        pallet_charge = 0.3
        skagerak_charge = 0.25
        
        additional_charges_toggle = st.toggle("Compulsory Charges", value=True)
        st.write(f"**Pallet Charge:** {pallet_charge} per kg")
        st.write(f"**Skagerak Terminal Charge:** {skagerak_charge} per kg")
        
        # Additional Processing Rates
        extra_charge = 0
        pro_rate=0
        prod_a_b_charge = 0.0
        descaling_charge = 0.0
        yield_value = st.session_state.get("yield_value", "N/A")
        st.write(f"**Yield Value:** {yield_value}")
        st.subheader("Optional Charges")
        if st.session_state.get("product") == "Fillet":
            prod_a_b = st.toggle("ProdA/B (1.00 per kg RM)", value=False)
            descaling = st.toggle("Descaling (1.50 per kg RM)", value=False)
            if prod_a_b:
                prod_a_b_charge = (1.00/yield_value)*100
            if descaling:
                descaling_charge = (1.50/yield_value)*100
        
        elif st.session_state.get("product") == "Portions":
            portion_skin_on = st.toggle("Portion Skin On (2.50 per kg)", value=False)
            portion_skinless = st.toggle("Portion Skinless (3.00 per kg)", value=False)
            if portion_skin_on:
                extra_charge += 2.50
            if portion_skinless:
                extra_charge += 3.00
        
         # Additional Freezing and Storage Charges
            
        if st.session_state.get("prod_type") == "Frozen":
            st.subheader("Frozen Charges")
            tunnel_freezing = st.toggle("Tunnel Freezing (1.65 per kg)", value=False)
            gyro_freezing = st.toggle("Gyro Freezing (2.00 per kg)", value=False)
            reception_fee = st.toggle("Reception Fee (0.15 per kg)", value=True)
            dispatch_fee = st.toggle("Dispatch Fee (0.15 per kg)", value=True)
            environmental_fee = st.toggle("Environmental Fee (3% of Total Rate)", value=True)
            electricity_fee = st.toggle("Electricity Fee (5% of Total Rate)", value=True)
            
            if tunnel_freezing:
                pro_rate += 1.65
            if gyro_freezing:
                pro_rate += 2.00
            # if environmental_fee:
            #     pro_rate += pro_rate * 0.03
            # if electricity_fee:
            #     pro_rate += pro_rate * 0.05
            # if reception_fee:
            #     pro_rate += 0.15
            # if dispatch_fee:
            #     pro_rate += 0.15
            if reception_fee:
                pro_rate += 0.15
            if dispatch_fee:
                pro_rate += 0.15
            if environmental_fee:
                env_rate = pro_rate * 0.03
            if electricity_fee:
                elec_rate = pro_rate * 0.05
            pro_rate = pro_rate + env_rate + elec_rate
            
        st.session_state["prod_a_b_charge"] = prod_a_b_charge
        st.session_state["descaling_charge"] = descaling_charge
        st.session_state["extra_charge"] = extra_charge
        st.session_state["pro_charge"] = pro_rate
    

# User Form
def user_form():
    st.subheader("Enquiry Form")

    product = st.selectbox("Product", ["Fillet", "Portions"], key="product")
    trim_type = st.selectbox("Trim Type", ["Trim A", "Trim B", "Trim C", "Trim D", "Trim E"], key="trim_type")
    rm_spec = st.selectbox("RM Spec", ["1-2 kg", "2-3 kg", "3-4 kg", "4-5 kg", "5-6 kg", "6-7 kg", "7-8 kg", "8-9 kg", "9+ kg"], key="rm_spec")
    yield_value = st.number_input("Yield", min_value=33.0, step=0.1, key="yield")
    prod_type = st.selectbox("Product Type", ["Fresh", "Frozen"], key="prod_type")
    pack = st.selectbox("Packaging Type", ["Corrugated Box","Solid Box", "EPS", "EPS AIR", "IVP", "Chain Pack 2R", "Chain Pack 3R", "Chain Pack 4R", "Chain Pack 5R"], key="pack")
    box_qty = st.selectbox("Packaging Size", ["5 kg", "10 kg", "15 kg AIR", "20 kg AIR", "20 kg", "VAC"], key="box_qty")
    transport_mode = st.selectbox("Mode of Transport", ["AIR", "regular"], key="transport_mode")
    st.session_state["yield_value"] = yield_value  
    # Fetch Rate per kg from MongoDB based on selected fields
    rate_data = rate_collection.find_one({
        "product": product,
        "trim_type": trim_type,
        "rm_spec": rm_spec
    }, {"rate_per_kg": 1, "_id": 0})

    rate_per_kg = rate_data["rate_per_kg"] if rate_data else "Rate not found"
    st.write(f"**Filleting Rate per kg:** {rate_per_kg}")

    # Fetch Packaging Rate per kg from MongoDB based on selected fields
    rate_pack = pack_collection.find_one({
        "prod_type": prod_type,
        "product": product,
        "box_qty": box_qty,
        "pack": pack,
        "transport_mode": transport_mode
    }, {"packaging_rate": 1, "_id": 0})
    
    packaging_rate = rate_pack["packaging_rate"] if rate_pack else "Select valid packaging options"
    st.write(f"**Packaging Rate per kg:** {packaging_rate}")

    extra_charge = st.session_state.get("extra_charge", 0)
    pro_charge = st.session_state.get("pro_charge", 0)
    prod_a_b_charge = st.session_state.get("prod_a_b_charge", 0)
    descaling_charge = st.session_state.get("descaling_charge", 0)
    

    
    if isinstance(packaging_rate, (int, float)) and isinstance(rate_per_kg, (int, float)):
        pro_rate = packaging_rate + rate_per_kg + 0.3 + 0.25 + extra_charge + prod_a_b_charge + descaling_charge # Including additional charges
        total_rate = pro_rate + pro_charge  # Including additional charges
        st.write(f"**Production Rate per kg (incl. additional charges):** {total_rate}")
    else:
        st.write("**Production Rate per kg:** Invalid rate data")

    
    if st.button("Submit Enquiry", key="submit_form"):
        data_collection.insert_one({
            "username": st.session_state["username"],
            "Product": product,
            "Trim Type": trim_type,
            "RM Spec": rm_spec,
            "Yield": yield_value,
            "Product Type": prod_type,
            "Box Type": box_qty,
            "Packaging": pack,
            "Transport": transport_mode,
            "Filleting Rate": rate_per_kg,
            "Packaging Rate": packaging_rate,
            "Pallet Charge": 0.3,
            "Skagerak Terminal Charge": 0.25,
            "Additional Processing Charges": extra_charge + prod_a_b_charge + descaling_charge + pro_charge,
            "Total Rate": total_rate
        })
        st.success("Form submitted successfully!")

# Orders Page
def user_orders():
    st.title("Submitted Enquiries Details")
    st.write("All submitted enquiries.")

    user_orders = list(data_collection.find({"username": st.session_state["username"]}, {"_id": 0, "username": 0}))
    if user_orders:
        st.table(user_orders)
    else:
        st.write("No orders found.")


######################
# Sidebar Navigation
st.sidebar.title("User Links")
if st.session_state["authenticated"]:
    if st.session_state["role"] == "admin":
        if st.sidebar.button("Admin Dashboard", key="admin_dashboard"):
            navigate("admin_dashboard")
    else:
        if st.sidebar.button("User Dashboard", key="user_dashboard"):
            navigate("user_dashboard")
        if st.sidebar.button("Enquiries", key="user_orders"):
            navigate("user_orders")
    
    if st.sidebar.button("Logout", key="logout"):
        st.session_state["authenticated"] = False
        st.session_state["username"] = ""
        navigate("login")
else:
    if st.sidebar.button("Login", key="sidebar_login"):
        navigate("login")
    if st.sidebar.button("Register", key="sidebar_register"):
        navigate("register")

# Page Routing
if st.session_state["authenticated"]:
    st.write(f"Welcome, {st.session_state['username']}!")  # Debugging message
    if st.session_state["page"] == "user_dashboard":
        user_dashboard()
    elif st.session_state["page"] == "admin_dashboard":
        admin_dashboard()
    elif st.session_state["page"] == "user_orders":
        user_orders()
else:
    st.warning("Please log in to continue.")  # Helps debug blank screen
    if st.session_state["page"] == "login":
        login()
    elif st.session_state["page"] == "register":
        register()
