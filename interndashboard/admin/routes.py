from flask import Blueprint, render_template, flash, redirect, url_for, session
from interndashboard import mysql
from interndashboard.users.routes import login_required

admin = Blueprint('admin', __name__, template_folder='templates')

# Admin
@admin.route('/studentsdashboard')
@login_required
def studentsdashboard():
    if session['studentnumber'] == 1:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM adminview')
        outputs = cur.fetchall()
        cur.close()
        return render_template('studentsdashboard.html', outputs=outputs)
    else:
        flash('You must be the admin to access that page...', 'danger')
        return redirect(url_for('main.home'))

# Admin view dashboard for a specific student
@admin.route('/studentdashboard/<studentnumber>')
@login_required
def studentdashboard(studentnumber):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM dashboard WHERE studentnumber=%s', [studentnumber])
    outputs = cur.fetchall()
    cur.close()
    curs = mysql.connection.cursor()
    curs.execute("SELECT * FROM topic_created WHERE studentnumber=%s", [studentnumber])
    results = curs.fetchall()
    cur.close()
    return render_template('dashboard.html', outputs=outputs, results=results)

# topics that needs to be approved or disapproved
@admin.route('/approvedisapprove/<studentnumber>')
@login_required
def approvedisapprove(studentnumber):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM dashboard WHERE studentnumber=%s', [studentnumber])
    outputs = cur.fetchall()
    cur.close()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM topic_created WHERE studentnumber=%s", [studentnumber])
    results = cur.fetchall()
    cur.close()
    return render_template('approvedisapprove.html', outputs=outputs, results=results)

# Move rows to another table
@admin.route('/approve/<studentnumber>/<topics>')
@login_required
def approve(studentnumber, topics):
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO dashboard(studentnumber, topics, description, startingdate, finishdate) SELECT * FROM topic_created WHERE studentnumber=%s and topics=%s',[studentnumber, topics])
    mysql.connection.commit()
    cur.execute('DELETE FROM topic_created WHERE studentnumber=%s and topics=%s',[studentnumber, topics])
    mysql.connection.commit()
    cur.execute('SELECT studentnumber FROM dashboard WHERE topics=%s and studentnumber=%s', [topics, studentnumber])
    studentnumber = cur.fetchone()
    cur.close()
    return redirect(url_for('admin.approvedisapprove', studentnumber=studentnumber['studentnumber']))
