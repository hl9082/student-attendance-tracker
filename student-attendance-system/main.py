import streamlit as st
import pandas as pd
from utils.auth import check_password
from utils.database import load_users
import os

st.set_page_config(
    page_title="Student Attendance System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("📚 Student Attendance System")

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.write("### Student Login")
        st.markdown("""
        Welcome to the Student Attendance System. Please log in with your credentials.

        New student? Go to the Register page to create your account.
        """)

        student_id = st.text_input("Student ID")
        password = st.text_input("Password", type="password")
        login_button = st.button("Login")

        if login_button:
            if check_password(student_id, password):
                st.session_state.logged_in = True
                st.session_state.student_id = student_id
                st.rerun()
            else:
                st.error("Invalid credentials")
    else:
        users_df = load_users()
        user = users_df[users_df['student_id'] == st.session_state.student_id].iloc[0]
        st.write(f"### Welcome, {user['name']}!")
        st.write(f"Class: {user['class_name']}")

        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

if __name__ == "__main__":
    main()
    os.system("streamlit run main.py --server.address 0.0.0.0 --server.port 8501")



