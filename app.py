import json
import smtplib
import sqlite3 as sql
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Flask, render_template, request, url_for, session
from werkzeug.utils import redirect

from flask_session import Session

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


def send_email(subject, receiver, message_text):
    sender_email = "mental.health@mrhconsult.co.za"
    password = "MrhHealth"
    receiver_email = receiver
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message.attach(MIMEText(message_text, "html"))
    e_session = smtplib.SMTP('mail.mrhconsult.co.za', 587)
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


def substance_calc(lst):
    m = 0
    for c in lst:
        if c == 'Y':
            m += 1
        else:
            m += 0

    if m < 2:
        msg = 'No symptoms for '
    elif 2 <= m <= 3:
        msg = 'Mild symptoms for '
    elif 4 <= m <= 5:
        msg = 'Moderate symptoms for '
    elif m >= 6:
        msg = 'Severe symptoms for '

    return msg


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about-you', methods=['GET', 'POST'])
def client():
    if request.method == 'POST':
        session['name'] = request.form['firstname'] + " " + request.form['lastname']
        session['email'] = request.form['email']
        subject = 'Mental Health Check'
        receiver = request.form['email']
        mail = f"""
            <!doctype html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport"
                      content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
                <meta http-equiv="X-UA-Compatible" content="ie=edge">
                <title>Document</title>
            </head>
            <body>
                <p>Hi, {session['name']} </p>
                <p>Thank you for visiting our website. We have captured your contact details and we will give you feedback soon.</p>
                <p>Kind regards,</p>
                <p>Mental Health Check</p>
            </body>
            </html>
            """
        if receiver != '':
            send_email(subject, receiver, mail)
        return redirect(url_for('additional'))
    return render_template('client_details.html')


@app.route('/initial-quiz', methods=('GET', 'POST'))
def additional():
    length = len(add_questions)
    quizzes = []
    if request.method == 'POST':
        answer1 = request.form['answer 0']
        answer2 = request.form['answer 1']
        answer3 = request.form['answer 2']
        answer4 = request.form['answer 3']
        answer5 = request.form['answer 4']
        answer6 = request.form['answer 5']
        answer7 = request.form['answer 6']
        if answer1 == 'Yes' or answer2 == 'Yes':
            link = "mental-quiz"
            name = "Depression Quiz"
            t = (link, name)
            quizzes.append(t)

        if answer3 == 'Yes' or answer4 == 'Yes':
            link = "alcohol-drug-quiz"
            name = "Past Alcohol or Drug Use Quiz"
            t = (link, name)
            quizzes.append(t)

        if answer6 == 'Yes' or answer7 == 'Yes':
            link = "anxiety-quiz"
            name = "Anxiety Quiz"
            t = (link, name)
            quizzes.append(t)

        if len(quizzes) == 0:
            return redirect(url_for('home'))
        else:
            return render_template("quizes.html", quizes=quizzes)
    return render_template('initial_questions.html', q=add_questions, len=length)


@app.route('/mental-quiz', methods=('GET', 'POST'))
def mental():
    ans_depression = []
    lens = len(questions[0])
    name = 'Depression Quiz'
    if request.method == 'POST':
        for i in range(lens):
            ans_depression.append(request.form[f'answer {i}'])
        diagnosis = depression_calc(ans_depression)
        session['mental_diagnosis'] = diagnosis
        return redirect(url_for('mental_result'))
    return render_template('quiz_1.html', questions=questions[0], len=lens, name=name)


@app.route('/anxiety-quiz', methods=('GET', 'POST'))
def anxiety():
    ans_anxiety = []
    lens = len(questions[1])
    name = 'Anxiety Quiz'
    if request.method == 'POST':
        for i in range(lens):
            ans_anxiety.append(request.form[f'answer {i}'])
        diagnosis = anxiety_calc(ans_anxiety)
        session['anxiety_diagnosis'] = diagnosis
        return redirect(url_for('anxiety_result'))
    return render_template('quiz_1.html', questions=questions[1], len=lens, name=name)


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
        sender_email = "mental.health@mrhconsult.co.za"
        contacts = 'Name: ' + name + '\n' + 'Email: ' + _email + '\n' + 'Phone: ' + phone + '\n\n'
        mail = f"""
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport"
                  content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
            <meta http-equiv="X-UA-Compatible" content="ie=edge">
            <title>Document</title>
        </head>
        <body>
            <p>Hi, </p>
            <p>I would like to book an appointment on: {text} </p>
            <p>My Contacts details are as follows:</p>
            <p>{contacts}</p>
        </body>
        </html>
        """
        send_email(subject, sender_email, mail)
        return redirect(url_for('home'))
    return render_template('contact.html')


@app.route('/self-assessment')
def assessments():
    return render_template('questionaire.html')


@app.route('/alcohol-drug-quiz', methods=('GET', 'POST'))
def alcohol_drugs():
    alcohol = []
    lens = len(questions[2])
    if request.method == 'POST':
        for i in range(lens):
            substance = request.form['drug']
            alcohol.append(request.form[f'answer {i}'])
        diagnosis = substance_calc(alcohol)
        session['substance_diagnosis'] = diagnosis + substance
        return redirect(url_for('substance_result'))
    return render_template('quiz_2.html', questions=questions[2], len=lens)


@app.route('/substance-abuse-results', methods=('GET', 'POST'))
def substance_result():
    diagnosis = session['substance_diagnosis']
    return render_template('results_substance.html', diagnosis=diagnosis)


if __name__ == '__main__':
    app.run(debug=True)
