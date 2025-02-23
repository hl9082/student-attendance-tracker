# Student Attendance System

A Streamlit-based attendance tracking system with biometric authentication capabilities. This system allows students to register, check in/out using simulated biometric verification, and view attendance reports.

## Features

- 🔐 Multi-factor biometric authentication (face, fingerprint, voice)
- 📝 Student registration with biometric data capture
- ✅ Daily attendance tracking (check-in/check-out)
- 📊 Comprehensive attendance reports
- 👥 Class-wise attendance monitoring
- 📱 Responsive web interface

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run main.py
```

## Project Structure

```
student-attendance-system/
├── .streamlit/              # Streamlit configuration
├── data/                    # Data storage
│   ├── attendance.csv      # Attendance records
│   └── users.csv           # User information
├── pages/                   # Streamlit pages
│   ├── attendance.py       # Attendance management
│   ├── register.py         # Student registration
│   └── reports.py          # Attendance reports
├── utils/                   # Utility functions
│   ├── auth.py             # Authentication functions
│   └── database.py         # Database operations
└── main.py                 # Main application entry
```

## Usage

1. **Registration**
   - New students can register with their basic information
   - Complete biometric data capture (face, fingerprint, voice)

2. **Attendance**
   - Check-in with biometric verification
   - Check-out with biometric verification
   - View daily attendance status

3. **Reports**
   - View attendance history
   - Class-wise attendance statistics
   - Daily attendance trends

## Security Features

- Multi-factor biometric authentication
- Secure password storage
- Session management
- Access control

## Technologies Used

- Python 3.11
- Streamlit
- Pandas
- NumPy
- Plotly

## Future Enhancements

- Real biometric hardware integration
- PostgreSQL database implementation
- Advanced reporting capabilities
- Multi-location support
