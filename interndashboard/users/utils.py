from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from interndashboard import mysql
from interndashboard.users.routes import login_required

utils = Blueprint('utils', __name__, template_folder='templates')

# Topic
@utils.route('/dashboard/<topics>')
@login_required
def dashboard_manipulate(topics):
    # Create a cursor
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM topic_created WHERE topics=%s", [topics])
    outputs = cur.fetchall()
    cur.close()
    if result > 0:
        return render_template('dashboard_manipulate.html', outputs=outputs)

# Edit
@utils.route('/edit/<topics>', methods=['POST', 'GET'])
@login_required
def edit(topics):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        topic = request.form['topics']
        description = request.form['description']
        startingdate = request.form['startingdate']
        finishdate = request.form['finishdate']
        cur.execute("UPDATE topic_created SET topics=%s, description=%s, startingdate=%s, finishdate=%s WHERE topics=%s", (topic, description, startingdate, finishdate, topics))
        # Commit DB
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('users.dashboard'))
    else:
        cur.execute('SELECT * FROM topic_created WHERE topics=%s', [topics])
        outputs = cur.fetchall()
        cur.close()
        return render_template('edit.html', outputs=outputs)

# Delete
@utils.route('/delete/<topics>')
@login_required
def delete(topics):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM topic_created WHERE topics=%s', [topics])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('users.dashboard'))

# Dashboard form
@utils.route('/createtopic/<studentnumber>', methods=['POST', 'GET'])
@login_required
def createtopic(studentnumber):
    if request.method == 'POST':
        topics = request.form['topics']
        startingdate = request.form['startingdate']
        finishdate = request.form['finishdate']
        description = request.form['description']
        # Create a cursor
        if startingdate < finishdate:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO topic_created(studentnumber, topics, description, startingdate, finishdate) VALUES(%s, %s, %s, %s, %s)", (studentnumber, topics, description, startingdate, finishdate))
            # Commit in DB
            mysql.connection.commit()
            # Close cur
            cur.close()
            if session["studentnumber"] == 1:
                return redirect(url_for('admin.approvedisapprove', studentnumber=studentnumber))
            return redirect(url_for('admin.studentdashboard', studentnumber = studentnumber))
        else:
            flash("Finish date has to be at least one day ahead of starting date", 'danger')
            return render_template('createtopic.html')
    return render_template('createtopic.html')
