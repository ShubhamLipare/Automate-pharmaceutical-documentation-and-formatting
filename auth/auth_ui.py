import streamlit as st
from auth.auth_service import AuthService

auth_service = AuthService()

def show_auth_page():

    st.title("🔐 Login / Signup")

    tab1, tab2 = st.tabs(["Login", "Signup"])

    with tab1:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            success, message = auth_service.login(username, password)
            if success:
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.success(message)
                st.rerun()
            else:
                st.error(message)

    with tab2:
        username = st.text_input("New Username", key="signup_user")
        password = st.text_input("New Password", type="password", key="signup_pass")

        if st.button("Signup"):
            success, message = auth_service.signup(username, password)
            if success:
                st.success(message)
            else:
                st.error(message)