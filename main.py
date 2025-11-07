from flask import Flask, render_template, request, redirect, url_for, session
import os
from werkzeug.utils import secure_filename
from utils.llms import get_resume_content, get_json_output, get_str_output, get_readiness_score, is_answer, get_interview_ques
from utils.stats import get_performance_score
from utils.verification import verify_public_badge
from utils.answer import get_transcription

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create it if it doesn’t exist

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

resume_path = 0


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload_resume', methods=['post'])
def upload_resume():
    if request.method == 'POST':
        resume = request.files['resume']
        filename = secure_filename(resume.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        desc = request.form['job_description']
        resume.save(filepath)
        global resume_path
        resume_path = filepath
        session['desc'] = desc

    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    content = get_resume_content(resume_path)
    json_content = get_json_output(content)
    session['content'] = json_content
    analysis_quote = get_str_output(content)
    readiness_score = get_readiness_score(content)
    performance = 0
    if json_content:
        if json_content['platform link']:
            performance = get_performance_score(json_content=json_content)
        n_crtf = len(json_content['certifications'])
    else:
        performance = None
    return render_template('dashboard.html', quote=analysis_quote, readiness_score=readiness_score, n_crtf=n_crtf, performance=performance)


@app.route('/dashboard/certificates')
def certificates():
    content = session['content']
    del session['content']
    if content['certificate links']:
        list = content['certificate links']
        count = 0
        for i in range(len(list)):
            if verify_public_badge(list[i]):
                count += 1
    else:
        count = 0
    return render_template('certificates.html', total_crtf=len(content['certifications']), crtf_count=count, pending_crtf=len(content['certifications'])-count, content=content)


# ---------------------------------------------------------

@app.route('/mock', methods=['GET', 'POST'])
def mock_interview():

    # --- POST: User is submitting an answer ---

    # --- GET: User needs to see a question ---

    # Check if the interview has been started.
    # 'interview_questions' is our new flag.
    if 'interview_questions' not in session:
        # Check if a description was just provided to start
        if 'desc' in session:
            # This is the first visit. Set up the interview.
            ques_list = get_interview_ques(session['desc'], 5)
            del session['desc']  # Clean up session

            session['interview_questions'] = ques_list
            session['current_q_index'] = 0
            session['user_answers'] = {}  # To store answers
        else:
            # User landed here directly. Send them to the start.
            # Change 'start_page' to your starting route
            return redirect(url_for('/'))

    # Get current state
    questions = session.get('interview_questions')
    current_index = session.get('current_q_index')

    # Check if interview is over
    if current_index >= len(questions):
        # Clear session data and show results
        answers = session.get('user_answers', {})
        # Clear the session for the next run
        session.pop('interview_questions', None)
        session.pop('current_q_index', None)
        session.pop('user_answers', None)

        # Go to a new results page
        return render_template('results.html', answers=answers)

    # Interview is in progress:
    # Get the current question to display
    current_question = questions[current_index]

    return render_template('mock.html',
                           current_ques=current_index,
                           n_ques=len(questions),
                           question=current_question)


@app.route('/api/mock-interview/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # 1. Get data from the form
        audio = request.files.get('audio')

        # 2. Get current state from session
        # Use .get() for safety, with a default
        current_index = session.get('current_q_index', 0)
        questions = session.get('interview_questions', [])

        if not questions:
            # This shouldn't happen if they started correctly, but good to check
            return redirect(url_for('/'))  # Or wherever your start page is

        # 3. Process the answer
        ans = get_transcription(audio)
        current_question = questions[current_index]

        # Store the answer (optional, but good for a summary page)
        if 'user_answers' not in session:
            session['user_answers'] = {}
        session['user_answers'][current_question] = ans

        # Process it (your is_answer function)
        check = is_answer(current_question, ans)

        if check:
            # 4. Increment the index for the *next* question
            session['current_q_index'] = current_index + 1

            # 5. Redirect back to this same route (will be a GET request)
            return redirect(url_for('mock_interview'), current_ques=current_index,
                            n_ques=len(questions),
                            question=current_question)


if __name__ == "__main__":
    app.run(debug=True)
