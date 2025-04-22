from flask import Flask, render_template_string, request, redirect, url_for, flash
from interview_scheduler import InterviewScheduler
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'interview_scheduler_secret_key'

scheduler = InterviewScheduler()

# HTML Templates as strings
INDEX_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interview Scheduler</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #f8f9fa; padding-top: 2rem; }
        .card { box-shadow: 0 4px 8px rgba(0,0,0,0.1); border-radius: 10px; border: none; }
        .form-control { border-radius: 8px; }
        .btn-primary { background-color: #4b6cb7; border: none; border-radius: 8px; }
        .btn-primary:hover { background-color: #3a539b; }
        .header-icon { font-size: 3rem; color: #4b6cb7; }
        .flash-messages { margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card mb-4 p-4">
                    <div class="card-body text-center">
                        <div class="header-icon mb-3">📅</div>
                        <h1 class="card-title mb-4">Interview Scheduler</h1>
                        
                        <div class="flash-messages">
                            {% with messages = get_flashed_messages(with_categories=true) %}
                                {% if messages %}
                                    {% for category, message in messages %}
                                        <div class="alert alert-{{ 'success' if category == 'success' else 'danger' }}">
                                            {{ message }}
                                        </div>
                                    {% endfor %}
                                {% endif %}
                            {% endwith %}
                        </div>
                        
                        <form action="{{ url_for('schedule') }}" method="post">
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <div class="form-group">
                                        <label for="candidate_slots"><strong>Candidate Available Slots</strong></label>
                                        <textarea id="candidate_slots" name="candidate_slots" class="form-control" rows="5" 
                                            placeholder="Enter one time slot per line&#10;Format: YYYY-MM-DD HH:MM">2025-04-22 10:00
2025-04-22 14:00
2025-04-23 11:00</textarea>
                                    </div>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <div class="form-group">
                                        <label for="interviewer_slots"><strong>Interviewer Available Slots</strong></label>
                                        <textarea id="interviewer_slots" name="interviewer_slots" class="form-control" rows="5" 
                                            placeholder="Enter one time slot per line&#10;Format: YYYY-MM-DD HH:MM">2025-04-22 14:00
2025-04-23 09:00
2025-04-23 11:00</textarea>
                                    </div>
                                </div>
                            </div>
                            <button type="submit" class="btn btn-primary btn-lg mt-3">Find Common Slots</button>
                        </form>
                    </div>
                </div>
                
                <div class="card p-4">
                    <div class="card-body">
                        <h4>Instructions</h4>
                        <p>Enter available time slots for both the candidate and interviewer, one slot per line.</p>
                        <p><strong>Format:</strong> YYYY-MM-DD HH:MM</p>
                        <p><strong>Example:</strong> 2025-04-22 14:00</p>
                        <p>The system will find common available slots and allow you to send confirmation emails.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''

RESULTS_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interview Scheduler - Results</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #f8f9fa; padding-top: 2rem; }
        .card { box-shadow: 0 4px 8px rgba(0,0,0,0.1); border-radius: 10px; border: none; margin-bottom: 20px; }
        .success-icon { font-size: 3rem; color: #28a745; margin-bottom: 1rem; }
        .time-slot { background-color: #e9f7ef; border-radius: 8px; padding: 15px; margin-bottom: 10px; transition: all 0.3s; }
        .time-slot:hover { background-color: #d5f5e3; transform: translateY(-2px); }
        .btn-primary { background-color: #4b6cb7; border: none; border-radius: 8px; }
        .btn-primary:hover { background-color: #3a539b; }
        .btn-outline-secondary { border-radius: 8px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card p-4">
                    <div class="card-body text-center">
                        <div class="success-icon">🎯</div>
                        <h1 class="card-title mb-4">Matching Slots Found!</h1>
                        <p class="lead mb-4">We found {{ common_slots|length }} common time slot(s) between the candidate and interviewer.</p>
                        
                        <div class="matching-slots mt-4">
                            <h4 class="mb-3">Common Available Slots:</h4>
                            {% for slot in common_slots %}
                                <div class="time-slot d-flex justify-content-between align-items-center">
                                    <div><strong>{{ slot }}</strong></div>
                                    <div>
                                        <button type="button" class="btn btn-primary" data-bs-toggle="modal" 
                                            data-bs-target="#emailModal" data-slot="{{ slot }}" data-index="{{ loop.index0 }}">
                                            Send Confirmation
                                        </button>
                                    </div>
                                </div>
                            {% endfor %}
                        </div>
                        
                        <div class="mt-4">
                            <a href="{{ url_for('index') }}" class="btn btn-outline-secondary">Back to Scheduler</a>
                        </div>
                    </div>
                </div>
                
                <div class="card p-4">
                    <div class="card-body">
                        <h4 class="mb-3">Input Summary</h4>
                        <div class="row">
                            <div class="col-md-6">
                                <h5>Candidate Slots:</h5>
                                <ul class="list-group">
                                    {% for slot in candidate_slots %}
                                        <li class="list-group-item">{{ slot }}</li>
                                    {% endfor %}
                                </ul>
                            </div>
                            <div class="col-md-6">
                                <h5>Interviewer Slots:</h5>
                                <ul class="list-group">
                                    {% for slot in interviewer_slots %}
                                        <li class="list-group-item">{{ slot }}</li>
                                    {% endfor %}
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Email Modal -->
    <div class="modal fade" id="emailModal" tabindex="-1" aria-labelledby="emailModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="emailModalLabel">Send Confirmation Email</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <form action="{{ url_for('send_confirmation') }}" method="post">
                    <div class="modal-body">
                        <input type="hidden" id="slot_index" name="slot_index" value="0">
                        <input type="hidden" id="slot" name="slot" value="">
                        <div class="mb-3">
                            <label for="email" class="form-label">Recipient Email Address</label>
                            <input type="email" class="form-control" id="email" name="email" required>
                        </div>
                        <div class="alert alert-info">
                            A confirmation email will be sent for the selected time slot.
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                        <button type="submit" class="btn btn-primary">Send Email</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        var emailModal = document.getElementById('emailModal')
        emailModal.addEventListener('show.bs.modal', function (event) {
            var button = event.relatedTarget
            var slotIndex = button.getAttribute('data-index')
            var slot = button.getAttribute('data-slot')
            document.getElementById('slot_index').value = slotIndex
            document.getElementById('slot').value = slot
        })
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(INDEX_TEMPLATE)

@app.route('/schedule', methods=['POST'])
def schedule():
    # Get time slots from form
    candidate_slots = request.form.get('candidate_slots', '').strip().split('\n')
    interviewer_slots = request.form.get('interviewer_slots', '').strip().split('\n')
    
    # Filter out empty slots
    candidate_slots = [slot.strip() for slot in candidate_slots if slot.strip()]
    interviewer_slots = [slot.strip() for slot in interviewer_slots if slot.strip()]
    
    if not candidate_slots or not interviewer_slots:
        flash('Please provide at least one time slot for both candidate and interviewer.', 'error')
        return redirect(url_for('index'))
    
    # Find common slots
    common_slots = scheduler.get_common_slots(candidate_slots, interviewer_slots)
    
    if not common_slots:
        flash('No common time slots found.', 'error')
        return redirect(url_for('index'))
    
    # Format slots for display
    formatted_slots = [slot.strftime('%Y-%m-%d %H:%M %Z') for slot in common_slots]
    
    return render_template_string(RESULTS_TEMPLATE, 
                         common_slots=formatted_slots,
                         candidate_slots=candidate_slots,
                         interviewer_slots=interviewer_slots)

@app.route('/send_confirmation', methods=['POST'])
def send_confirmation():
    slot_index = int(request.form.get('slot_index', 0))
    email = request.form.get('email', '').strip()
    slot_str = request.form.get('slot', '').strip()
    
    if not email:
        flash('Please provide an email address.', 'error')
        return redirect(url_for('index'))
    
    # Parse the slot string back to datetime
    try:
        slot_str_clean = slot_str.rsplit(' ', 1)[0]
        slot = scheduler.validate_time_slot(slot_str_clean)
        if slot is None:
            raise ValueError("Invalid time format")
    except (ValueError, TypeError, IndexError):
        flash('Invalid time slot format.', 'error')
        return redirect(url_for('index'))
    
    # Send confirmation email
    success = scheduler.send_confirmation_email(email, slot)
    
    if success:
        flash('Confirmation email sent successfully!', 'success')
    else:
        flash('Failed to send confirmation email. Please check your email configuration.', 'error')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True) 