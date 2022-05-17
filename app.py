import json
import sqlite3 as sql

from flask import Flask, render_template, request, url_for, session, flash
from werkzeug.utils import redirect
from flask_session import Session

app = Flask(__name__)
app.secret_key = b'_5#y2L"FFF4Q8z\n\xec]/'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

with open("depression.json", "r") as read_file:
    questions = json.load(read_file)
ans_depression = []


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
        msg = 'Diagnosis: Minimal depression'
    elif 5 <= m <= 9:
        msg = 'Diagnosis: Mild depression'
    elif 10 <= m <= 14:
        msg = 'Diagnosis: Moderate depression'
    elif 15 <= m <= 19:
        msg = 'Diagnosis: Moderately severe depression'
    elif 20 <= m <= 27:
        msg = 'Diagnosis: Severe depression'

    return msg


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/client', methods=['GET', 'POST'])
def client():
    if request.method == 'POST':
        session['name'] = request.form['firstname']
        session['lastname'] = request.form['lastname']
        session['cell'] = request.form['cell']
        session['email'] = request.form['email']
        session['age'] = request.form['age']
        session['gender'] = request.form['gender']
        session['rank'] = request.form['rank']
        session['race'] = request.form['race']
        session['province'] = request.form['province']
        session['postal'] = request.form['postal']
        session['marital'] = request.form['marital']
        session['address'] = request.form['addr1'] + ', ' + request.form['addr2'] + ', ' + request.form['city']
        session['education'] = request.form['education']
        session['years employed'] = request.form['years employed']
        session['training'] = request.form['training']
        session['religion'] = request.form['religion']

        save_to_db()
        return redirect(url_for('additional'))

    return render_template('client_details.html')


@app.route('/book-appointment', methods=('GET', 'POST'))
def book():
    if request.method == 'POST':
        session['name'] = request.form['firstname']
        session['lastname'] = request.form['lastname']
        session['cell'] = request.form['cell']
        session['email'] = request.form['email']
        session['age'] = request.form['age']
        session['gender'] = request.form['gender']
        session['rank'] = request.form['rank']
        session['race'] = request.form['race']
        session['province'] = request.form['province']
        session['postal'] = request.form['postal']
        session['marital'] = request.form['marital']
        session['address'] = request.form['addr1'] + ', ' + request.form['addr2'] + ', ' + request.form['city']
        session['education'] = request.form['education']
        session['years employed'] = request.form['years employed']
        session['training'] = request.form['training']
        session['religion'] = request.form['religion']

        save_to_db()
        return redirect(url_for('home'))
    return render_template('book_appointment.html')


@app.route('/additional-info_1', methods=('GET', 'POST'))
def additional():
    if request.method == 'POST':
        answer1 = request.form['answer 0']
        answer2 = request.form['answer 1']
        if answer1 == 'Yes' or answer2 == 'Yes':
            try:
                select_mental_1 = request.form.getlist('specify 0')
                select_mental_2 = request.form.getlist('specify 1')
            except ValueError:
                return redirect(url_for('mental'))
            return redirect(url_for('mental'))
        else:
            return redirect(url_for('home'))
    return render_template('additional_mental_illness.html')


@app.route('/mental-quiz', methods=('GET', 'POST'))
def mental():
    lens = len(questions)
    if request.method == 'POST':
        for i in range(lens):
            ans_depression.append(request.form[f'answer {i}'])
        diagnosis = depression_calc(ans_depression)
        session['mental_diagnosis'] = diagnosis
        return redirect(url_for('mental_result'))
    return render_template('quiz_depression.html', questions=questions, len=lens)


@app.route('/mental-results', methods=('GET', 'POST'))
def mental_result():
    diagnosis = session['mental_diagnosis']
    return render_template('results_mental.html', diagnosis=diagnosis)
