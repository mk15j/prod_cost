import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Production Cost Calculator", layout="wide")

# --- DATA DICTIONARIES ---
packaging_rates = {
    "Fresh, Fillet, 10 kg, EPS Box & Ice": 2.00,
    "Fresh, Fillet, 20 kg, EPS Box & Ice": 2.50,
    "Fresh, Fillet, 15 kg AIR, EPS Box & Gel-Pack/Dry-Ice": 4.00,
    "Fresh, Fillet, 20 kg AIR, EPS Box & Gel-Pack/Dry-Ice": 4.00,
    "Fresh, Fillet, 2-3 kg, Vacuum Pack": 4.00,
    "Fresh, Fillet, 3-4 kg, Vacuum Pack": 3.50,
    "Fresh, Fillet, 4-5 kg, Vacuum Pack": 3.25,
    "Fresh, Fillet, 5-6 kg, Vacuum Pack": 3.00,
    "Fresh, Portion, All, IVP": 3.5,
    "Fresh, Portion, All, Chain Pack (2) with Rider": 4.25,
    "Fresh, Portion, All, Chain Pack (3) with Rider": 5.50,
    "Fresh, Portion, All, Chain Pack (4) with Rider": 4.25,
    "Fresh, Portion, All, Chain Pack (5) with Rider": 4.25,
    "Frozen, Fillet, 10 kg, EPS Box & Ice": 2.00,
    "Frozen, Fillet, 20 kg, EPS Box & Ice": 2.5,
    "Frozen, Fillet, 2-3 kg, Vacuum Pack": 4.00,
    "Frozen, Fillet, 3-4 kg, Vacuum Pack": 3.50,
    "Frozen, Fillet, 4-5 kg, Vacuum Pack": 3.25,
    "Frozen, Fillet, 5-6 kg, Vacuum Pack": 3.00,
    "Frozen, Portion, All, IVP": 3.50,
    "Frozen, Portion, All, Chain Pack (2) with Rider": 4.25,
    "Frozen, Portion, All, Chain Pack (3) with Rider": 5.50,
    "Frozen, Portion, All, Chain Pack (4) with Rider": 4.25,
    "Frozen, Portion, All, Chain Pack (5) with Rider": 4.25,
    "Frozen, Fillet, 20 kg, Solid Box": 1.75,
    "Frozen, Fillet, 10 kg, Corrugated Box": 2.00,
    "Frozen, Fillet, 5 kg, Corrugated Box": 2.25,
    "Frozen, Portion, 20 kg, Solid Box": 1.75,
    "Frozen, Portion, 10 kg, Corrugated Box": 2.00,
    "Frozen, Portion, 5 kg, Corrugated Box": 2.25,
}

trim_rates = {
    "1-2 kg, Trim A": 14.2,
    "2-3 kg, Trim A": 5.7,
    "3-4 kg, Trim A": 3.95,
    "4-5 kg, Trim A": 3.45,
    "5-6 kg, Trim A": 2.95,
    "6-7 kg, Trim A": 2.95,
    "7-8 kg, Trim A": 3.97,
    "8-9 kg, Trim A": 3.95,
    "> 9 kg, Trim A": 3.95,
    "1-2 kg, Trim B": 15.2,
    "2-3 kg, Trim B": 5.95,
    "3-4 kg, Trim B": 4.2,
    "4-5 kg, Trim B": 3.7,
    "5-6 kg, Trim B": 3.2,
    "6-7 kg, Trim B": 3.2,
    "7-8 kg, Trim B": 4.2,
    "8-9 kg, Trim B": 4.2,
    "> 9 kg, Trim B": 4.2,
    "1-2 kg, Trim C": 15.7,
    "2-3 kg, Trim C": 6.2,
    "3-4 kg, Trim C": 4.45,
    "4-5 kg, Trim C": 3.95,
    "5-6 kg, Trim C": 3.45,
    "6-7 kg, Trim C": 3.45,
    "7-8 kg, Trim C": 4.45,
    "8-9 kg, Trim C": 4.45,
    "> 9 kg, Trim C": 4.45,
    "1-2 kg, Trim D": 17.7,
    "2-3 kg, Trim D": 6.45,
    "3-4 kg, Trim D": 4.7,
    "4-5 kg, Trim D": 4.2,
    "5-6 kg, Trim D": 3.7,
    "6-7 kg, Trim D": 3.7,
    "7-8 kg, Trim D": 4.7,
    "8-9 kg, Trim D": 4.7,
    "> 9 kg, Trim D": 4.7,
    "1-2 kg, Trim E": 20.7,
    "2-3 kg, Trim E": 7.7,
    "3-4 kg, Trim E": 5.95,
    "4-5 kg, Trim E": 5.45,
    "5-6 kg, Trim E": 4.95,
    "6-7 kg, Trim E": 4.95,
    "7-8 kg, Trim E": 5.95,
    "8-9 kg, Trim E": 5.95,
    "> 9 kg, Trim E": 5.95,

}
packaging_options = {
    "Fresh, Fillet": {
        "specifications": ["10 kg", "20 kg", "15 kg AIR", "20 kg AIR", "2-3 kg", "3-4 kg", "4-5 kg", "5-6 kg"],
        "materials": ["EPS Box & Ice", "EPS Box & Gel-Pack/Dry-Ice", "Vacuum Pack"]
    },
    "Fresh, Portion": {
        "specifications": ["All"],
        "materials": ["IVP", "Chain Pack (2) with Rider", "Chain Pack (3) with Rider", "Chain Pack (4) with Rider", "Chain Pack (5) with Rider"]
    },
    "Frozen, Fillet": {
        "specifications": ["10 kg", "20 kg", "5 kg", "2-3 kg", "3-4 kg", "4-5 kg", "5-6 kg"],
        "materials": ["EPS Box & Ice", "Vacuum Pack", "Solid Box", "Corrugated Box"]
    },
    "Frozen, Portion": {
        "specifications": ["20 kg", "10 kg", "5 kg", "All"],
        "materials": ["Solid Box", "Corrugated Box", "IVP", "Chain Pack (2) with Rider", "Chain Pack (3) with Rider", "Chain Pack (4) with Rider", "Chain Pack (5) with Rider"]
    }
}

# --- PAGE TITLE ---
st.title("🚀 Production Cost Calculator")

# --- SIDEBAR NAVIGATION ---

st.sidebar.title("Links")
st.sidebar.markdown("[📋 Skagerak Calculator](#)")
st.sidebar.markdown("[⚙ Settings](#)")

# --- TOGGLE BUTTONS ---
col1, col2 = st.columns(2)
with col1:
    is_fresh = st.toggle("Fresh", value=False)
with col2:
    is_frozen = st.toggle("Frozen", value=False)

if is_fresh and is_frozen:
    st.warning("Please select either Fresh or Frozen, not both.")
    st.stop()
elif not is_fresh and not is_frozen:
    st.warning("Please select either Fresh or Frozen.")
    st.stop()
##
# --- ADDITIONAL RATES FOR FROZEN ---
additional_rates = {
    "Prod A/Prod B": 1.00,
    "Descaling": 1.50,
    "Tunnel Freezing": 1.65,
    "Gyro Freezing": 2.00,
    "Environmental Fee": 0.03,
    "Electricity Fee": 0.05,
    "Portions SkinOn": 2.50,
    "Portions SkinLess": 3.00,
}
toggle_states = {}
if is_frozen:
    st.subheader("⚙️ Additional Rates for Frozen Products")
    for key in additional_rates:
        toggle_states[key] = st.toggle(key, value=False)
else:
    st.subheader("⚙️ Additional Rates for Fresh Products")
    for key in ["Prod A/Prod B", "Descaling", "Portions SkinOn", "Portions SkinLess"]:
        toggle_states[key] = st.toggle(key, value=False)

# Ensure mutually exclusive toggles
if toggle_states["Portions SkinOn"] and toggle_states["Portions SkinLess"]:
    st.warning("Please select either SkinOn or SkinLess, not both.")
    st.stop()
# --- PRODUCT SELECTION ---
st.subheader("📦 Packaging Details")
product = st.selectbox("Product", ["Select...", "Fillet", "Portion"])

packaging_spec = None
packaging_material = None
selected_category = None  # Ensure it's always defined

if product != "Select...":
    product_type = "Fresh" if is_fresh else "Frozen"
    selected_category = f"{product_type}, {product}"
    
    if selected_category in packaging_options:
        packaging_spec = st.selectbox("Packaging Specification", ["Select..."] + packaging_options[selected_category]["specifications"])
        packaging_material = st.selectbox("Packaging Material", ["Select..."] + packaging_options[selected_category]["materials"])
    else:
        st.warning("Invalid selection, please choose again.")
else:
    st.warning("Please select a product to see packaging options.")

# --- RAW MATERIAL DETAILS ---
st.subheader("🔍 Raw Material Details")
rm_spec = st.selectbox("Select RM Spec", ["Select...", "1-2 kg", "2-3 kg", "3-4 kg", "4-5 kg", "5-6 kg", "6-7 kg", "7-8 kg", "8-9 kg", ">9 kg"])
trim_type = st.selectbox("Select Trim Type", ["Select...", "Trim A", "Trim B", "Trim C", "Trim D", "Trim E"])

# --- Ensure Valid Selections Before Processing ---
if product and packaging_spec and packaging_material != "Select...":
    packaging_key = f"{selected_category}, {packaging_spec}, {packaging_material}"
    packaging_rate = packaging_rates.get(packaging_key, 0)
else:
    packaging_key = None
    # packaging_rate = 0

if rm_spec != "Select..." and trim_type != "Select...":
    trim_key = f"{rm_spec}, {trim_type}"
    trim_rate = trim_rates.get(trim_key, 0)
else:
    trim_key = None
    # trim_rate = 0

# --- INPUTS FOR CALCULATION ---
quantity = st.number_input("Enter RM Quantity (kg)", min_value=1000.00, step=0.10)
yield_percentage = st.number_input("Enter Yield Percentage (%)", min_value=0.0, max_value=100.0, value=50.0, step=0.1)
fg_qty = quantity * (yield_percentage / 100)
terminal_value = 0.25

# if st.button("🔢 Calculate Production Cost"):
#     if packaging_rate == 0 or trim_rate == 0:
#         st.warning("⚠️ Packaging or Trim rate not found. Please check your selections.")
#     else:
#         extra_costs = sum(value for key, value in additional_rates.items() if toggle_states.get(key, False))
#         production_cost = ((packaging_rate + extra_costs) * fg_qty + (trim_rate + terminal_value) * fg_qty)

#         st.success(f"✅ Production Cost: **{production_cost:.2f}**")
        
#         with st.expander("📝 Cost Breakdown"):
#             st.write(f"Packaging Rate: {packaging_rate:.2f}")
#             st.write(f"Fillet and Trim Rate: {trim_rate:.2f}")
#             for key, value in additional_rates.items():
#                 if toggle_states.get(key, False):
#                     st.write(f"{key}: {value:.2f}")
#             st.write(f"Terminal Fee: {terminal_value:.2f}")

            ###########
if st.button("🔢 Calculate Production Cost"):
    if packaging_rate == 0 or trim_rate == 0:
        st.warning("⚠️ Packaging or Trim rate not found. Please check your selections.")
    else:
        # Calculate additional costs
        prod_a_b_cost = additional_rates["Prod A/Prod B"] * quantity if toggle_states.get("Prod A/Prod B", False) else 0
        descaling_cost = additional_rates["Descaling"] * quantity if toggle_states.get("Descaling", False) else 0

        # Sum up extra costs excluding Environmental Fee & Electricity Fee
        extra_costs = sum(
            value for key, value in additional_rates.items()
            if key not in ["Prod A/Prod B", "Descaling", "Environmental Fee", "Electricity Fee"] and toggle_states.get(key, False)
        )

        # Initial Production Cost
        production_cost = ((packaging_rate + extra_costs) * fg_qty + (trim_rate + terminal_value) * fg_qty + prod_a_b_cost + descaling_cost)

        # Apply Environmental and Electricity Fees
        env_fee = production_cost * additional_rates["Environmental Fee"] if toggle_states.get("Environmental Fee", False) else 0
        elec_fee = production_cost * additional_rates["Electricity Fee"] if toggle_states.get("Electricity Fee", False) else 0

        # Final Production Cost
        total_production_cost = production_cost + env_fee + elec_fee

        st.success(f"✅ Production Cost: **{total_production_cost:.2f}**")

        with st.expander("📝 Cost Breakdown"):
            st.write(f"Packaging Rate: {packaging_rate:.2f}")
            st.write(f"Fillet and Trim Rate: {trim_rate:.2f}")
            st.write(f"Prod A / Prod B Rate: {prod_a_b_cost/quantity:.2f}")
            st.write(f"Descaling Cost: {descaling_cost:.2f}")
            for key, value in additional_rates.items():
                if toggle_states.get(key, False) and key not in ["Environmental Fee", "Electricity Fee"]:
                    st.write(f"{key}: {value:.2f}")
            st.write(f"Environmental Fee: {env_fee:.2f}")
            st.write(f"Electricity Fee: {elec_fee:.2f}")
            st.write(f"Terminal Fee: {terminal_value:.2f}")

            ######

