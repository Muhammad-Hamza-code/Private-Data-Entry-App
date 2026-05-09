import streamlit as st
import pandas as pd

# Set page config
st.set_page_config(page_title="School Directory Manager", layout="wide")

# ==========================================
# AUTHENTICATION SETUP
# ==========================================
# Define the list of emails that are allowed to access the app
ALLOWED_EMAILS = [
    "ezlabsproducts@gmail.com",
    "meetmunazza212010@gmail.com"
] # Replace these with your actual authorized emails

# Initialize login state
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Display Login Screen if not logged in
if not st.session_state['logged_in']:
    st.title("🔒 Access Restricted")
    st.write("You must enter an authorized email address to access the directory.")
    
    with st.form("login_form"):
        email_input = st.text_input("Email Address", placeholder="Enter your email...")
        submit_login = st.form_submit_button("Log In")
        
        if submit_login:
            if email_input.lower().strip() in ALLOWED_EMAILS:
                st.session_state['logged_in'] = True
                st.session_state['current_user'] = email_input.lower().strip()
                st.success("Access Granted! Redirecting...")
                st.rerun()
            else:
                st.error("Access Denied: This email is not authorized.")
    
    # Stop the script here so the rest of the app doesn't load
    st.stop()

# ==========================================
# MAIN APP CODE (Only runs if logged in)
# ==========================================

# Initialize session state for data persistence (in-memory)
if 'school_data' not in st.session_state:
    initial_data = [
        ["Hira School Sukkur Township", "Not given", "House no 29, Imam Bargha, Street no 03", "7:30 AM - 1:30 PM", "(071) 5633459"],
        ["Beaconhouse Sukkur Campus", "info@soe.edu.pk", "Friends Co-operative Housing Society", "8:00 AM - 4:00 PM", "(071) 5633459"],
        ["School of Excellence Sukkur", "feedback@bh.edu.pk", "PR7P+D2Q, G.E.C.H.S., Sukkur", "7:00 AM - 9:00 PM", "(071) 5804400"],
        ["The City School Indus Campus", "csnmro22@csn.edu.pk", "Survay no 258, Indus Valley, near Taj filling", "7:30 AM - 4:00 PM", "(071) 5824044"],
        ["Queen Mary School Sukkur", "qmschoolsukkur@gmail.com", "By pass road, near Sukkur Township", "Not given", "0300-8313715"],
        ["The Spirit School Sukkur", "info@insirer.edu.pk", "Near Maki Shah Pir, Opposite DC office", "Not given", "0316-3118811"],
        ["Allied Schools Society Campus", "Not given", "Sindhi Muslim Society, Near Bhatti Office", "Not given", "0311-2274579"],
        ["Army Public School Sukkur", "APSACS Secretariat", "Sukkur Cantt", "8:00 AM - 2:00 PM", "(071) 5628511"],
        ["The Smart School (Indus)", "smartinfo@thesmartschools.edu.pk", "Banglow #32, Sector 1, Sukkur Township", "Not given", "0330-2384999"],
        ["Arqam Public High School", "sukkurarqamschool@gmail.com", "Main Road, Sukkur, Sindh", "8:00 AM - 5:00 PM", "(071) 5818351"],
        ["The Lahore Lyceum School", "thelyceum1to8@gmail.com", "Kot Mahmood, Pakistan", "8:00 AM - 5:00 PM", "0323-4545588"],
        ["Lahore American School", "Not given", "15 Canal Rd, Upper Mall Scheme, Lahore", "7:30 AM - 3:30 PM", "(042) 35762506"],
        ["Roots International School", "Not given", "EME Society, Lahore", "8:00 AM - 2:30 PM", "+92 51 111-747-747"]
    ]
    st.session_state.school_data = pd.DataFrame(initial_data, columns=["School Name", "Email", "Address", "Timing", "Phone"])

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["View Directory", "Add New School", "Remove School"])

st.sidebar.markdown("---")
st.sidebar.write(f"Logged in as: **{st.session_state['current_user']}**")

# Logout functionality
if st.sidebar.button("Logout"):
    st.session_state['logged_in'] = False
    st.session_state['current_user'] = None
    st.rerun()

# --- VIEW DIRECTORY ---
if page == "View Directory":
    st.title("🏫 School Directory Database")
    st.write("Current list of schools in Pakistan.")
    
    # EXACT SCHOOL NAME SEARCH FUNCTIONALITY
    search_query = st.text_input("🔍 Search specifically by School Name", placeholder="Type a school name here...")
    df = st.session_state.school_data
    
    if search_query:
        # This explicitly targets only the "School Name" column
        df = df[df["School Name"].str.contains(search_query, case=False, na=False)]
        
        if df.empty:
            st.warning(f"No schools found matching '{search_query}'.")
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Export options
    st.download_button(
        label="Download as CSV",
        data=df.to_csv(index=False),
        file_name="school_directory.csv",
        mime="text/csv"
    )

# --- ADD NEW SCHOOL ---
elif page == "Add New School":
    st.title("➕ Add New School Entry")
    st.write("Use the form below to add a new school to the database.")
    
    with st.form("add_school_form", clear_on_submit=True):
        name = st.text_input("School Name", placeholder="e.g. Sukkur Grammar School")
        email = st.text_input("Email Address", placeholder="e.g. info@school.edu.pk")
        address = st.text_area("Complete Address", placeholder="Street, Sector, City...")
        timing = st.text_input("Operational Hours", placeholder="e.g. 8:00 AM - 2:00 PM")
        phone = st.text_input("Contact Phone Number", placeholder="e.g. (071) 1234567")
        
        submit_button = st.form_submit_button("Save School to Directory")
        
        if submit_button:
            if name:
                new_row = pd.DataFrame([[name, email, address, timing, phone]], 
                                     columns=["School Name", "Email", "Address", "Timing", "Phone"])
                st.session_state.school_data = pd.concat([st.session_state.school_data, new_row], ignore_index=True)
                st.success(f"Successfully added {name}!")
            else:
                st.error("School Name is a required field.")

# --- REMOVE SCHOOL ---
elif page == "Remove School":
    st.title("🗑️ Remove School Entry")
    st.write("Select a school from the list to remove it permanently.")
    
    school_list = st.session_state.school_data["School Name"].tolist()
    school_to_remove = st.selectbox("Select School to Delete", school_list)
    
    if st.button("Delete Selected School", type="primary"):
        st.session_state.school_data = st.session_state.school_data[
            st.session_state.school_data["School Name"] != school_to_remove
        ].reset_index(drop=True)
        st.warning(f"Removed {school_to_remove} from the database.")
        st.rerun()

# Footer
st.sidebar.markdown("---")
st.sidebar.info("EZ School Management Module - v1.0")