# Interview Scheduler

A Flask-based web application for scheduling interviews by finding common available time slots between candidates and interviewers.

## Features
- Input available time slots for candidates and interviewers
- Automatically find common available time slots
- Send email confirmations for scheduled interviews
- User-friendly interface with Bootstrap styling
- Timezone support

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/uuganbolor0419/interview-scheduler-.git
cd interview-scheduler-
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
- Copy `.env.example` to `.env`
- Update `.env` with your email settings:
  ```
  EMAIL_SENDER=your-email@gmail.com
  EMAIL_PASSWORD=your-app-password
  SMTP_SERVER=smtp.gmail.com
  SMTP_PORT=465
  TIMEZONE=UTC
  ```

5. Run the application:
```bash
python app.py
```

6. Access the application at: http://localhost:5000

## Email Configuration
To enable email functionality:
1. Use a Gmail account
2. Enable 2-Step Verification in your Google Account
3. Generate an App Password for the application
4. Use the App Password in your `.env` file

## Technologies Used
- Python
- Flask
- Bootstrap
- Gmail SMTP
