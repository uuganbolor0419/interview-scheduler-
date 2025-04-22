# Automated Interview Scheduler (Basic Demo)
from datetime import datetime
from typing import List, Dict, Optional
from dateutil import parser
import pytz
import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

class InterviewScheduler:
    def __init__(self):
        load_dotenv()  # Load environment variables
        self.timezone = pytz.timezone(os.getenv('TIMEZONE', 'UTC'))
        self.email_sender = os.getenv('EMAIL_SENDER')
        self.email_password = os.getenv('EMAIL_PASSWORD')
        self.smtp_server = os.getenv('SMTP_SERVER')
        self.smtp_port = int(os.getenv('SMTP_PORT', 465))
        
        # Print settings for debugging (without password)
        print(f"Email Configuration:")
        print(f"Sender: {self.email_sender}")
        print(f"SMTP Server: {self.smtp_server}")
        print(f"SMTP Port: {self.smtp_port}")

    def validate_time_slot(self, time_slot: str) -> Optional[datetime]:
        """Validate and parse a time slot string into a datetime object."""
        try:
            dt = parser.parse(time_slot)
            if dt.tzinfo is None:
                dt = self.timezone.localize(dt)
            return dt
        except (ValueError, TypeError):
            return None

    def get_common_slots(self, candidate_slots: List[str], interviewer_slots: List[str]) -> List[datetime]:
        """Find common available time slots between candidate and interviewer."""
        valid_candidate_slots = [self.validate_time_slot(slot) for slot in candidate_slots]
        valid_interviewer_slots = [self.validate_time_slot(slot) for slot in interviewer_slots]
        
        # Filter out invalid slots
        valid_candidate_slots = [slot for slot in valid_candidate_slots if slot is not None]
        valid_interviewer_slots = [slot for slot in valid_interviewer_slots if slot is not None]
        
        # Convert to sets for intersection
        candidate_set = set(valid_candidate_slots)
        interviewer_set = set(valid_interviewer_slots)
        
        return sorted(list(candidate_set & interviewer_set))

    def send_confirmation_email(self, to_email: str, slot: datetime) -> bool:
        """Send a confirmation email for the interview slot."""
        try:
            print(f"\nAttempting to send email to: {to_email}")
            print(f"For slot: {slot.strftime('%Y-%m-%d %H:%M %Z')}")

            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.email_sender
            msg['To'] = to_email
            msg['Subject'] = 'Interview Slot Confirmation'

            body = f"""
            Hello,

            Your interview has been scheduled for: {slot.strftime('%Y-%m-%d %H:%M %Z')}

            Please make sure to be available at the scheduled time.

            Best regards,
            Interview Scheduler
            """
            msg.attach(MIMEText(body, 'plain'))

            # Create secure SSL context
            context = ssl.create_default_context()

            print("Connecting to SMTP server...")
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
                print("Logging in...")
                server.login(self.email_sender, self.email_password)
                print("Sending email...")
                server.send_message(msg)
                print("Email sent successfully!")
                return True

        except smtplib.SMTPAuthenticationError as e:
            print(f"Authentication failed. Please check your email and app password: {str(e)}")
            return False
        except smtplib.SMTPException as e:
            print(f"SMTP error occurred: {str(e)}")
            return False
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            print(f"Error type: {type(e)}")
            return False

if __name__ == "__main__":
    scheduler = InterviewScheduler()
