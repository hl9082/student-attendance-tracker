import streamlit as st
from utils.auth import capture_biometric_data
from utils.database import save_user
import time

def app():
    st.title("👤 New Student Registration")

    # Initialize form data in session state
    if 'registration_step' not in st.session_state:
        st.session_state.registration_step = 1

    # Step 1: Basic Information
    if st.session_state.registration_step == 1:
        student_id = st.text_input("Student ID")
        name = st.text_input("Full Name")
        password = st.text_input("Password", type="password")
        class_name = st.selectbox("Class", [
            "Class A", "Class B", "Class C", "Class D", "Class E"
        ])

        next_button = st.button("Next: Biometric Registration")

        if next_button and student_id and name and password and class_name:
            st.session_state.student_id = student_id
            st.session_state.name = name
            st.session_state.password = password
            st.session_state.class_name = class_name
            st.session_state.registration_step = 2
            st.rerun()
        elif next_button:
            st.error("Please fill all fields")

    # Step 2: Biometric Registration
    elif st.session_state.registration_step == 2:
        st.write("### Biometric Data Collection")
        st.write("Please enable your camera and microphone for biometric registration.")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.camera_input("Face Recognition", key="face_input")

        with col2:
            st.write("Place your finger on the scanner")
            fingerprint_btn = st.button("Scan Fingerprint", key="fingerprint_btn")

        with col3:
            st.write("Voice Recognition")
            voice_btn = st.button("Record Voice Sample", key="voice_btn")
            if voice_btn:
                st.write("🎤 Recording... Speak your name clearly")
                with st.spinner("Processing voice sample..."):
                    time.sleep(2)
                    st.success("Voice sample recorded! ✅")

        complete_reg = st.button("Complete Registration", key="complete_reg")
        if complete_reg:
            if st.session_state.get('face_input') is not None:
                with st.spinner("Registering biometric data..."):
                    biometric_data = capture_biometric_data()
                    if biometric_data:
                        save_user(
                            st.session_state.student_id,
                            st.session_state.name,
                            st.session_state.password,
                            st.session_state.class_name,
                            biometric_data
                        )
                        st.success("Registration successful! 🎉")
                        st.balloons()
                        # Reset registration step
                        st.session_state.registration_step = 1
                        # Clear stored form data
                        for key in ['student_id', 'name', 'password', 'class_name']:
                            if key in st.session_state:
                                del st.session_state[key]
            else:
                st.error("Please complete face recognition capture")

        back_btn = st.button("Back", key="back_btn")
        if back_btn:
            st.session_state.registration_step = 1
            st.rerun()

if __name__ == "__main__":
    app()