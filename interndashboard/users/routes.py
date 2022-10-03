from flask import Blueprint, request, flash, redirect, url_for, render_template, session
from ..models import *
from ..extensions import db
from passlib.hash import sha256_crypt
import pandas as pd
import json
import plotly
import plotly.express as px
from functools import wraps

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
    print(User.query.all())
    if request.method == 'POST':
        studentnumber = request.form['studentnumber']
        firstname = request.form['firstname']
        surname = request.form['surname']
        major = request.form['major']
        degree = request.form['degree']
        studentmail = request.form['studentmail']
        password = request.form['password']
        confirmpassword = request.form['confirmpassword']
        print(password)
        print()
        print(confirmpassword)

        if password == confirmpassword:
            user = User(studentnumber=studentnumber, firstname=firstname, surname=surname, major=major, degree=degree, studentmail=studentmail, password=password)
            db.session.add(user)
            db.session.commit()

            flash('Successfully signed up', 'success')
            return redirect(url_for('users.signin'))
        else:
            flash('Passwords do not match', 'danger')
            return redirect(request.url)

    return render_template('signup.html')

# Sign in
@users.route('/signin', methods=['POST', 'GET'])
def signin():
    if request.method == 'POST':
        studentnumber = request.form['studentnumber']
        password = request.form['password']

        user = User.query.filter_by(studentnumber=studentnumber).first()
        if user:
            if user.password == password:
                session['loggedin'] = True
                session['studentnumber'] = user.studentnumber
                session['firstname'] = user.firstname
                flash('You are logged in', 'success')
                return redirect(url_for('main.home'))
            else:
                flash('Wrong password', 'danger')
                return redirect(request.url)
        else:
            flash('User do not exit', 'danger')
            return redirect(request.url)
    
    return render_template('signin.html')

# Log out
@users.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('users.signin'))

# Student dashboard
@users.route('/dashboard/<studentnumber>')
@login_required
def dashboard(studentnumber):
    user = db.session.execute(db.select(User).filter_by(studentnumber=session['studentnumber'])).scalar()
    print(user.studentnumber)

    # Dashboard of approved topics
    outputs = Dashboard.query.filter_by(studentnumber=session['studentnumber']).all()
    # outputs = db.session.execute(db.select(Dashboard).filter_by(studentnumber=session['studentnumber'])).scalar()
    print(outputs)
 
    # Dashboard that has to be approved
    topics = Topic_create.query.filter_by(studentnumber=studentnumber).all()
    print(topics)
    
    # # For dashboard graph
    # cur.execute('SELECT * FROM dashgraph WHERE studentnumber=%s', [session['studentnumber']])
    # datas = cur.fetchall()

    # df = pd.DataFrame(datas)
    # fig1 = px.timeline(df, x_start='startingdate', x_end='finishdate', y='topics', color='percentages')
    # fig1.update_yaxes(autorange='reversed')
    # graph1json = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

    if outputs != None or topics != None:
        return render_template('dashboard.html', user=user, outputs=outputs, topics=topics)
    else:
        flash('Dashboard is empty', 'danger')
        return render_template('dashboard.html', user=user, outputs=outputs, topics=topics)