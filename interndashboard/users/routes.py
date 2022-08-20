from flask import Blueprint, request, flash, redirect, url_for, render_template, session
from passlib.hash import sha256_crypt
import pandas as pd
import json
import plotly
import plotly.express as px
from functools import wraps
from interndashboard import mysql

users = Blueprint('users', __name__, template_folder='templates')

# Controls login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'loggedin' in session:
            return f(*args, **kwargs)
        flash("Unauthorized access, please sign in!", 'danger')
        return redirect(url_for('users.signin'))
    return decorated_function

# Signup path
@users.route('/signup', methods=["POST", "GET"])
def signup():
    if request.method == 'POST':
        studentnumber = request.form['studentnumber']
        firstname = request.form['firstname']
        surname = request.form['surname']
        major = request.form['major']
        degree = request.form['degree']
        studentmail = request.form['studentmail']
        password = sha256_crypt.encrypt(request.form['password'])
        # Create a cursor
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO signup(studentnumber, firstname, surname, major, degree, studentmail, mypassword) VALUES(%s, %s, %s, %s, %s, %s, %s)", (studentnumber, firstname, surname, major, degree, studentmail, password))
        # Commit to DB
        mysql.connection.commit()
        # Close connection
        cur.close()
        flash('Successfully signed up', 'success')
        return redirect(url_for('users.signin'))

    return render_template('signup.html')

# Sign in
@users.route('/signin', methods=['POST', 'GET'])
def signin():
    if request.method == 'POST':
        studentnumber = request.form['studentnumber']
        password = request.form['password']
        # Create a cursor
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM signup WHERE studentnumber=%s", [studentnumber])
        if result > 0:
            users = cur.fetchone()
            mypassword = users['mypassword']
            # Close connection
            cur.close()
            if sha256_crypt.verify(password, mypassword):
                session['loggedin'] = True
                session['studentnumber'] = users['studentnumber']
                session['firstname'] = users['firstname']
                flash('You are logged in', 'success')
                return redirect(url_for('main.home'))
            else:
                flash('Wrong password', 'danger')
                return redirect(url_for('users.signin'))
        else:
            flash('User do not exist', 'danger')
            return redirect(url_for('users.signin'))
    
    return render_template('signin.html')

# Log out
@users.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('users.signin'))

# Student dashboard
@users.route('/dashboard/')
@login_required
def dashboard():
    # Dashboard of approved topics
    cur = mysql.connection.cursor()
    rlt = cur.execute("SELECT * FROM dashboard WHERE studentnumber=%s", [session['studentnumber']])
    outputs = cur.fetchall()

    # Dashboard that has to be approved
    rslts = cur.execute('SELECT * FROM topic_created WHERE studentnumber=%s', [session['studentnumber']])
    results = cur.fetchall()
    
    # For dashboard graph
    cur.execute('SELECT * FROM dashgraph WHERE studentnumber=%s', [session['studentnumber']])
    datas = cur.fetchall()
    cur.close()

    df = pd.DataFrame(datas)
    fig1 = px.timeline(df, x_start='startingdate', x_end='finishdate', y='topics', color='percentages')
    fig1.update_yaxes(autorange='reversed')
    graph1json = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

    if rlt > 0 or rslts > 0:
        return render_template('dashboard.html', outputs=outputs, results=results, graph1json=graph1json)
    else:
        flash('Dashboard is empty', 'danger')
        return render_template('dashboard.html')