from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey


app = Flask(__name__)


app.config['SECRET_KEY'] = "debug123"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


@app.route('/')
def home():
    return render_template('home.html', survey_title=satisfaction_survey.title,
                           survey_instructions=satisfaction_survey.instructions)


@app.route('/store-answers')
def update_answers():
    session['answers'] = []
    session['question_count'] = 0
    return redirect(f"/question/{session['question_count']}")


@app.route('/question/<int:q>')
def show_question(q):
    if session['question_count'] >= len(satisfaction_survey.questions):
        return redirect('/thank-you')
    if q == session['question_count']:
        question = satisfaction_survey.questions[q].question
        choices = satisfaction_survey.questions[q].choices
        return render_template('question.html', question=question, choices=choices)
    else:
        flash("Invalid question order - please complete this question first!")
        return redirect(f"/question/{session['question_count']}")


@app.route('/thank-you')
def thank_you():
    return render_template('thank-you.html', survey_title=satisfaction_survey.title)


@app.route('/answer', methods=['POST'])
def answer():
    session['question_count'] += 1
    session['answers'].append(request.form['choice'])
    return redirect(f"/question/{session['question_count']}")