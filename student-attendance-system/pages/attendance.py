import streamlit as st
import pandas as pd
from utils.auth import simulate_biometric_scan
from utils.database import log_attendance, load_attendance
from datetime import datetime

def app():
    st.title("🕒 Attendance Management")

    if not st.session_state.get('logged_in', False):
        st.warning("Please login first")
        st.stop()

    attendance_df = load_attendance()
    today = datetime.now().strftime('%Y-%m-%d')
    today_record = attendance_df[
        (attendance_df['student_id'] == st.session_state.student_id) & 
        (attendance_df['date'] == today)
    ]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Check In")
        camera_on = st.camera_input("Face Recognition for Check-In")

        if st.button("Complete Check-In", key="check_in_btn"):
            if not today_record.empty and not pd.isna(today_record.iloc[0]['check_in']):
                st.error("Already checked in today!")
            else:
                if camera_on is not None:
                    st.write("### Biometric Verification")
                    with st.spinner("Verifying biometric data..."):
                        success, methods = simulate_biometric_scan()
                        if success:
                            log_attendance(st.session_state.student_id, methods, check_in=True)
                            st.success("Check-in successful! ✅")
                            st.balloons()
                else:
                    st.error("Please enable camera for face recognition")

    with col2:
        st.subheader("Check Out")
        camera_out = st.camera_input("Face Recognition for Check-Out")

        if st.button("Complete Check-Out", key="check_out_btn"):
            if today_record.empty or pd.isna(today_record.iloc[0]['check_in']):
                st.error("Please check-in first!")
            elif not pd.isna(today_record.iloc[0]['check_out']):
                st.error("Already checked out today!")
            else:
                if camera_out is not None:
                    st.write("### Biometric Verification")
                    with st.spinner("Verifying biometric data..."):
                        success, methods = simulate_biometric_scan()
                        if success:
                            log_attendance(st.session_state.student_id, methods, check_in=False)
                            st.success("Check-out successful! ✅")
                            st.balloons()
                else:
                    st.error("Please enable camera for face recognition")

if __name__ == "__main__":
    app()