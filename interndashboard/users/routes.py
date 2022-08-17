from flask import Blueprint, request, flash, redirect, url_for, render_template, session
from passlib.hash import sha256_crypt
from interndashboard import mysql

users = Blueprint('users', __name__, template_folder='templates')

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
            data = cur.fetchone()
            mypassword = data['mypassword']
            # Close connection
            cur.close()
            if sha256_crypt.verify(password, mypassword):
                session['loggedin'] = True
                session['studentnumber'] = data['studentnumber']
                session['firstname'] = data['firstname']
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
# @loggin_required
def logout():
    session.clear()
    return redirect(url_for('users.signin'))

# Student dashboard
@users.route('/dashboard/')
# @loggin_required
def dashboard():
    # Create a cursor
    cur = mysql.connection.cursor()
    rlt = cur.execute("SELECT * FROM dashboard WHERE studentnumber=%s", [session['studentnumber']])
    outputs = cur.fetchall()

    cur.close()
    curs = mysql.connection.cursor()
    rslts = curs.execute('SELECT * FROM topic_created WHERE studentnumber=%s', [session['studentnumber']])
    results = curs.fetchall()
    curs.close()
    if rlt > 0 or rslts > 0:
        return render_template('dashboard.html', outputs=outputs, results=results)
    else:
        flash('Dashboard is empty', 'danger')
        return render_template('dashboard.html')