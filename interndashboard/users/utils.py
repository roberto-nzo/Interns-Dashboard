from turtle import update
from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from interndashboard.users.routes import login_required
from ..models import *
from datetime import datetime, date

utils = Blueprint('utils', __name__, template_folder='templates')

# Topic
@utils.route('/temp_dashboard/<id>/<topics>')
@login_required
def dashboard_manipulate(topics, id):
    results = Topic_create.query.filter_by(id=id).first()
    return render_template('dashboard_manipulate.html', outputs=results)

# Edit
@utils.route('/edit/<id>/<topics>', methods=['POST', 'GET'])
@login_required
def edit(topics, id):
    if request.method == 'POST':
        topic = request.form['topics']
        description = request.form['description']
        startingdate_data = request.form['startingdate']
        finishdate_data = request.form['finishdate']
        startingdate = datetime.strptime(startingdate_data, '%Y-%m-%d').date()
        finishdate = datetime.strptime(finishdate_data, '%Y-%m-%d').date()
        
        
        new = Topic_create.query.filter_by(id=id).first()
        new.topic = topic
        new.description = description
        new.startingdate = startingdate
        new.finishdate = finishdate
        db.session.commit()
        user = User.query.filter_by(studentnumber=new.studentnumber).first()
        if session['studentnumber'] == user.studentnumber:
            return redirect(url_for('users.dashboard', id=new.id, studentnumber=new.studentnumber))
        else:
            return redirect(url_for('admin.approvedisapprove', studentnumber=new.studentnumber))
    else:
        outputs = Topic_create.query.filter_by(id=id).first()
        check = Topic_create.query.filter_by(id=id).first()
        print(check.description)
        
        return render_template('edit.html', outputs=outputs)

# Delete
@utils.route('/delete/<id>/<topics>')
@login_required
def delete(topics, id):
    topic = Topic_create.query.filter_by(id=id).first()
    user = User.query.filter_by(studentnumber=topic.studentnumber).first()
    db.session.delete(topic)
    db.session.commit()
    # Dashboard.
    if session['studentnumber'] == 1:
        return redirect(url_for('admin.approvedisapprove', studentnumber=user.studentnumber))
    else:
        return redirect(url_for('users.dashboard', studentnumber=user.studentnumber))

# Dashboard form
@utils.route('/createtopic/<studentnumber>', methods=['POST', 'GET'])
@login_required
def createtopic(studentnumber):
    if request.method == 'POST':
        topics = request.form['topics']
        startingdate_data = request.form['startingdate']
        finishdate_data = request.form['finishdate']
        description = request.form['description']
        startingdate = datetime.strptime(startingdate_data, '%Y-%m-%d').date()
        finishdate = datetime.strptime(finishdate_data, '%Y-%m-%d').date()

        if startingdate < finishdate:
            topic = Topic_create(studentnumber=studentnumber, topics=topics, description=description, startingdate=startingdate, finishdate=finishdate)
            db.session.add(topic)
            db.session.commit()
            
            if session["studentnumber"] == 1:
                return redirect(url_for('admin.approvedisapprove', studentnumber=studentnumber))
            return redirect(url_for('users.dashboard', studentnumber = studentnumber))
        else:
            flash("Finish date has to be at least one day ahead of starting date", 'danger')
            return render_template('createtopic.html')
    return render_template('createtopic.html', studentnumber=studentnumber)
