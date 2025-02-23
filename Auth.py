import streamlit as st
from pages.stream_app.utils import setup_page

def auth_page():
    setup_page("🔐 Authentication", sidebar_state="collapsed")
    
    if 'authenticated' in st.session_state and st.session_state['authenticated']:
        st.switch_page("pages/2_📒_Notebooks.py")
        st.stop()

    st.title("Welcome to Open Notebook")
    
    tab1, tab2 = st.tabs(["Sign In", "Register"])
    
    with tab1:
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Sign In")
            
            if submit:
                # For demo purposes, using a simple check
                if email == "demo@example.com" and password == "password":
                    st.session_state['authenticated'] = True
                    st.session_state['user'] = {'email': email}
                    st.success("Login successful!")
                    st.switch_page("pages/1_🏠_Home.py")
                else:
                    st.error("Invalid credentials")

    with tab2:
        with st.form("register_form"):
            new_email = st.text_input("Email")
            new_password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            submit = st.form_submit_button("Register")
            
            if submit:
                if new_password != confirm_password:
                    st.error("Passwords don't match")
                else:
                    st.success("Registration successful! Please sign in.")

if __name__ == "__main__":
    auth_page()