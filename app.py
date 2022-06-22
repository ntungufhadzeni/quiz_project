import json
import sqlite3 as sql
from datetime import datetime

from flask import Flask, render_template, request, url_for, session, flash
from werkzeug.utils import redirect
from flask_session import Session

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)
app.static_folder = 'static'
app.secret_key = b'_5#y2L"FFF4Q8z\n\xec]/'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


with open("questions.json", "r") as read_file:
    questions = json.load(read_file)

with open("add_data_file.json", "r") as read_file:
    add_questions = json.load(read_file)

ans_depression = []
ans_anxiety = []


def send_email(subject, message_text):
    sender_email = ""
    password = ""
    receiver_email = ""
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message.attach(MIMEText(message_text, 'plain'))
    e_session = smtplib.SMTP('smtp.gmail.com', 587)
    e_session.starttls()
    e_session.login(sender_email, password)
    text = message.as_string()
    e_session.sendmail(sender_email, receiver_email, text)
    e_session.quit()


def save_to_db():
    con = sql.connect("clients.db")
    cur = con.cursor()

    cur.execute("""INSERT INTO clients (first_name,last_name,cell,email,age,gender,rank,race,address,
                            province,postal,marital,education,years_employed,training,religion) 
                            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (session['name'], session['lastname'], session['cell'], session['email'], session['age'],
                 session['gender'], session['rank'], session['race'], session['address'], session['province'],
                 session['postal'], session['marital'], session['education'], session['years employed'],
                 session['training'], session['religion']))
    con.commit()
    con.close()


def depression_calc(lst):
    m = 0
    for c in lst:
        if c == 'A':
            m += 0
        elif c == 'B':
            m += 1
        elif c == 'C':
            m += 2
        elif c == 'D':
            m += 3
    if 0 <= m <= 4:
        msg = 'Minimal depression'
    elif 5 <= m <= 9:
        msg = 'Mild depression'
    elif 10 <= m <= 14:
        msg = 'Moderate depression'
    elif 15 <= m <= 19:
        msg = 'Moderately severe depression'
    elif 20 <= m <= 27:
        msg = 'Severe depression'

    return msg


def anxiety_calc(lst):
    m = 0
    for c in lst:
        if c == 'A':
            m += 0
        elif c == 'B':
            m += 1
        elif c == 'C':
            m += 2
        elif c == 'D':
            m += 3
    if 0 <= m <= 4:
        msg = 'Minimal anxiety'
    elif 5 <= m <= 9:
        msg = 'Mild anxiety'
    elif 10 <= m <= 14:
        msg = 'Moderate anxiety'
    elif 15 <= m <= 21:
        msg = 'Severe anxiety'

    return msg


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about-you', methods=['GET', 'POST'])
def client():
    if request.method == 'POST':
        name = request.form['firstname']
        return redirect(url_for('additional'))

    return render_template('client_details.html')


@app.route('/initial-quiz', methods=('GET', 'POST'))
def additional():
    length = len(add_questions)
    quizes = []
    if request.method == 'POST':
        answer1 = request.form['answer 0']
        answer2 = request.form['answer 1']
        answer3 = request.form['answer 2']
        answer4 = request.form['answer 3']
        if answer1 == 'Yes' or answer2 == 'Yes':
            link = "mental-quiz"
            name = "Depression Quiz"
            t = (link, name)
            quizes.append(t)

        if answer3 == 'Yes' or answer4 == 'Yes':
            link = "anxiety-quiz"
            name = "Anxiety Quiz"
            t = (link, name)
            quizes.append(t)

        if len(quizes) == 0:
            return redirect(url_for('home'))
        else:
            return render_template("quizes.html", quizes=quizes)
    return render_template('initial_questions.html', q=add_questions, len=length)


@app.route('/mental-quiz', methods=('GET', 'POST'))
def mental():
    lens = len(questions[0])
    if request.method == 'POST':
        for i in range(lens):
            ans_depression.append(request.form[f'answer {i}'])
        diagnosis = depression_calc(ans_depression)
        session['mental_diagnosis'] = diagnosis
        return redirect(url_for('mental_result'))
    return render_template('quiz_1.html', questions=questions[0], len=lens)


@app.route('/anxiety-quiz', methods=('GET', 'POST'))
def anxiety():
    lens = len(questions[1])
    if request.method == 'POST':
        for i in range(lens):
            ans_anxiety.append(request.form[f'answer {i}'])
        diagnosis = anxiety_calc(ans_anxiety)
        session['anxiety_diagnosis'] = diagnosis
        return redirect(url_for('anxiety_result'))
    return render_template('quiz_1.html', questions=questions[1], len=lens)


@app.route('/mental-results', methods=('GET', 'POST'))
def mental_result():
    diagnosis = session['mental_diagnosis']
    return render_template('results_mental.html', diagnosis=diagnosis)


@app.route('/anxiety-results', methods=('GET', 'POST'))
def anxiety_result():
    diagnosis = session['anxiety_diagnosis']
    return render_template('results_anxiety.html', diagnosis=diagnosis)


@app.route('/contact-us', methods=('GET', 'POST'))
def contact():
    if request.method == 'POST':
        subject = 'Mental Health Check'
        name = request.form['name']
        phone = request.form['phone']
        _email = request.form['email']
        text = request.form['message']
        message = 'Name: ' + name + '\n' + 'Email: ' + _email + '\n' + 'Phone: ' + phone + '\n' + text
        # send_email(subject, message)
        message = 'Message received, we will get back to you soon'
        flash(message)
        return redirect(url_for('home'))
    return render_template('contact.html')


@app.route('/self-assessment')
def assessments():
    return render_template('questionaire.html')


if __name__ == '__main__':
    app.run(debug=True)