from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

RESPONSES_KEY = 'responses'


@app.route('/')
def show_survey_start():
    """Show start page & form."""
    return render_template("start.html", survey=satisfaction_survey)


@app.route('/begin', methods=["POST"])
def start_survey():
    """Clear the session of responses."""
    session[RESPONSES_KEY] = []
    return redirect("/questions/0")


@app.route("/questions/<int:qid>")
def show_question(qid):
    """Display current question."""
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        return redirect("/")
    elif (len(responses) == len(satisfaction_survey.questions)):
        return redirect("/complete")
    elif (len(responses) != qid):
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")

    question = satisfaction_survey.questions[qid]
    return render_template("question.html", question_num=qid, question=question)


@app.route("/answer", methods=["POST"])
def handle_answer():
    """Save response and redirect to next question."""
    choice = request.form['answer']
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses
    if (len(responses) == len(satisfaction_survey.questions)):
        return redirect("/complete")
    else:
        return redirect(f"/questions/{len(responses)}")


@app.route("/complete")
def complete():
    """Survey complete. Show completion page."""
    return render_template("completion.html")

# if __name__ == '__main__':
#     app.run(debug=True)

# responses = []
