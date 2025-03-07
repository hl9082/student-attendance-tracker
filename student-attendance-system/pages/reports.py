import streamlit as st
import pandas as pd
import plotly.express as px
from utils.database import load_attendance, load_users
from datetime import datetime, timedelta

def app():
    st.title("📈 Attendance Reports")

    if not st.session_state.get('logged_in', False):
        st.warning("Please login first")
        st.stop()

    attendance_df = load_attendance()
    users_df = load_users()

    # Date range selector
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "Start Date",
            datetime.now() - timedelta(days=30)
        )
    with col2:
        end_date = st.date_input(
            "End Date",
            datetime.now()
        )

    # Filter data by date range
    mask = (attendance_df['date'] >= start_date.strftime('%Y-%m-%d')) & \
           (attendance_df['date'] <= end_date.strftime('%Y-%m-%d'))
    filtered_df = attendance_df[mask]

    # Merge with user data
    report_df = filtered_df.merge(users_df[['student_id', 'name', 'class_name']], on='student_id')

    # Summary statistics
    st.subheader("Summary Statistics")
    total_days = (end_date - start_date).days + 1
    attendance_count = report_df.groupby('student_id').size()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Working Days", total_days)
    with col2:
        st.metric("Total Students", len(users_df))
    with col3:
        st.metric("Average Attendance", f"{attendance_count.mean():.1f} days")

    # Class-wise attendance
    st.subheader("Class-wise Attendance")
    class_attendance = report_df.groupby('class_name').size().reset_index()
    class_attendance.columns = ['Class', 'Attendance Count']
    fig = px.bar(class_attendance, x='Class', y='Attendance Count',
                 title="Attendance by Class")
    st.plotly_chart(fig)

    # Daily attendance trend
    st.subheader("Daily Attendance Trend")
    daily_attendance = report_df.groupby('date').size().reset_index()
    daily_attendance.columns = ['Date', 'Attendance Count']
    fig = px.line(daily_attendance, x='Date', y='Attendance Count',
                  title="Daily Attendance Trend")
    st.plotly_chart(fig)

    # Detailed attendance records
    st.subheader("Detailed Attendance Records")
    st.dataframe(report_df[['date', 'name', 'class_name', 'check_in', 'check_out']])

if __name__ == "__main__":
    app()
