from flask import Flask, render_template, redirect, flash, request
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey


app = Flask(__name__)
app.config['SECRET_KEY'] = "Pineapple24"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = list()

@app.route('/')
def home_page():
    return render_template("home.html", survey = survey)

@app.route('/questions/<question_num>')
def get_next_question(question_num):
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
    responses.append(choice)
    return redirect(f'/questions/{len(responses)}')

@app.route("/thanks")
def thank_you():
    return render_template("thanks.html")
