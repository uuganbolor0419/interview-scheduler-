# Interview Scheduler

A Python-based interview scheduling system that helps match available time slots between candidates and interviewers.

## Features

- Time slot validation and parsing
- Automatic matching of common available slots
- Email confirmation system
- Timezone support
- Configuration management

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and configure your email settings:
   ```bash
   cp .env.example .env
   ```
4. Edit `.env` with your email credentials:
   - For Gmail, you'll need to use an App Password
   - You can generate an App Password by following [Google's instructions](https://support.google.com/accounts/answer/185833)

## Usage

1. Import the `InterviewScheduler` class:
   ```python
   from interview_scheduler import InterviewScheduler
   ```

2. Create an instance of the scheduler:
   ```python
   scheduler = InterviewScheduler()
   ```

3. Define available time slots for candidate and interviewer:
   ```python
   candidate_slots = [
       "2025-04-22 10:00",
       "2025-04-22 14:00",
       "2025-04-23 11:00"
   ]
   
   interviewer_slots = [
       "2025-04-22 14:00",
       "2025-04-23 09:00",
       "2025-04-23 11:00"
   ]
   ```

4. Find common slots:
   ```python
   common_slots = scheduler.get_common_slots(candidate_slots, interviewer_slots)
   ```

5. Send confirmation email (optional):
   ```python
   if common_slots:
       selected_slot = common_slots[0]
       scheduler.send_confirmation_email("candidate@example.com", selected_slot)
   ```

## Time Format

Time slots should be provided in the format: `YYYY-MM-DD HH:MM`
Example: `2025-04-22 14:00`

## Contributing

Feel free to submit issues and enhancement requests! 