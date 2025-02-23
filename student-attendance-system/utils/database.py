import pandas as pd
import os
from datetime import datetime

def ensure_data_files():
    """Create data files if they don't exist"""
    if not os.path.exists('data'):
        os.makedirs('data')

    if not os.path.exists('data/users.csv'):
        pd.DataFrame(columns=[
            'student_id', 'name', 'password', 'class_name',
            'biometric_data', 'voice_data', 'registration_date'
        ]).to_csv('data/users.csv', index=False)

    if not os.path.exists('data/attendance.csv'):
        pd.DataFrame(columns=[
            'student_id', 'date', 'class_name', 'check_in', 'check_out',
            'verification_method'
        ]).to_csv('data/attendance.csv', index=False)

def load_users():
    ensure_data_files()
    return pd.read_csv('data/users.csv')

def load_attendance():
    ensure_data_files()
    return pd.read_csv('data/attendance.csv')

def save_user(student_id, name, password, class_name, biometric_data, voice_data=None):
    users_df = load_users()
    new_user = pd.DataFrame([{
        'student_id': student_id,
        'name': name,
        'password': password,
        'class_name': class_name,
        'biometric_data': biometric_data,
        'voice_data': voice_data,
        'registration_date': datetime.now().strftime('%Y-%m-%d')
    }])
    users_df = pd.concat([users_df, new_user], ignore_index=True)
    users_df.to_csv('data/users.csv', index=False)

def log_attendance(student_id, verification_method, check_in=True):
    attendance_df = load_attendance()
    users_df = load_users()
    user = users_df[users_df['student_id'] == student_id].iloc[0]
    today = datetime.now().strftime('%Y-%m-%d')

    if check_in:
        new_attendance = pd.DataFrame([{
            'student_id': student_id,
            'date': today,
            'class_name': user['class_name'],
            'check_in': datetime.now().strftime('%H:%M:%S'),
            'check_out': None,
            'verification_method': verification_method
        }])
        attendance_df = pd.concat([attendance_df, new_attendance], ignore_index=True)
    else:
        mask = (attendance_df['student_id'] == student_id) & (attendance_df['date'] == today)
        attendance_df.loc[mask, 'check_out'] = datetime.now().strftime('%H:%M:%S')

    attendance_df.to_csv('data/attendance.csv', index=False)