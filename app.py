from flask import Flask, render_template, redirect, flash, request, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey


app = Flask(__name__)
app.config['SECRET_KEY'] = "Pineapple24"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

@app.route('/')
def home_page():
    return render_template("home.html", survey = survey)

@app.route('/start', methods=["POST"])
def set_session():
    session['responses'] = list()
    return redirect('/questions/0')

@app.route('/questions/<question_num>')
def get_next_question(question_num):
    responses = session.get('responses')
    if int(len(responses)) == int(len(survey.questions)):
        return redirect ('/thanks')
    if int(question_num) != int(len(responses)):
        flash(f"Invalid question id: {question_num}")
        return redirect (f'/questions/{int(len(responses))}')
    question = survey.questions[int(question_num)]
    return render_template("questions.html", survey = survey, question = question)

@app.route("/answers", methods=["POST"])
def handle_question():
    choice = request.form['answer']
    list = session['responses']
    list.append(choice)
    session['responses'] = list
    return redirect(f'/questions/{len(list)}')

@app.route("/thanks")
def thank_you():
    return render_template("thanks.html")
