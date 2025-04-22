# Automated Interview Scheduler (Basic Demo)
from datetime import datetime
from typing import List, Dict, Optional
from dateutil import parser
import pytz

class InterviewScheduler:
    def __init__(self):
        self.timezone = pytz.timezone('UTC')  # Default to UTC, can be configured

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
        """Simulate sending a confirmation email."""
        # For demo purposes, just return True
        return True

if __name__ == "__main__":
    scheduler = InterviewScheduler()
