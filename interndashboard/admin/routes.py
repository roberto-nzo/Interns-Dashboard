from flask import Blueprint, render_template, flash, redirect, url_for, session, request
import json
import pandas as pd
import plotly
import plotly.express as px
from interndashboard.users.routes import login_required
from ..models import *

admin = Blueprint('admin', __name__, template_folder='templates')

# Admin
@admin.route('/studentsdashboard')
@login_required
def studentsdashboard():
    if session['studentnumber'] == 1:
        outputs = User.query.filter(User.studentnumber!=1).all()
        
        return render_template('studentsdashboard.html', outputs=outputs)
    else:
        flash('Access denied', 'danger')
        return redirect(url_for('main.home'))


# topics that needs to be approved or disapproved
@admin.route('/approvedisapprove/<studentnumber>')
@login_required
def approvedisapprove(studentnumber):
    if session['studentnumber'] == 1:
        user = User.query.filter_by(studentnumber=studentnumber).first_or_404()
        outputs = Dashboard.query.filter_by(studentnumber=studentnumber).all()
        
        results = Topic_create.query.filter_by(studentnumber=studentnumber).all()
        
        # # Display dashboard graph of the student
        # cur.execute('SELECT * FROM dashgraph WHERE studentnumber=%s', [studentnumber])
        # datas = cur.fetchall()
        # cur.close()
        
        # df = pd.DataFrame(datas)
        # fig1 = px.timeline(df, x_start='startingdate', x_end='finishdate', y='topics', color='percentages')
        # graph1json = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
        return render_template('approvedisapprove.html', user=user, outputs=outputs, results=results)
    else:
        flash('Access denied...', 'danger')
        return redirect(request.url)

# Move rows to another table
@admin.route('/approve/<id>/<studentnumber>/<topics>')
@login_required
def approve(studentnumber, topics, id):
    if session['studentnumber'] == 1:
        topic = Topic_create.query.filter_by(id=id).first_or_404()
        dash = Dashboard(studentnumber=topic.studentnumber, topics=topic.topics, description=topic.description, startingdate=topic.startingdate, finishdate=topic.finishdate)
        db.session.add(dash)
        db.session.commit()
        db.session.delete(topic)
        db.session.commit()

        return redirect(url_for('admin.approvedisapprove', studentnumber=studentnumber))
    else:
        flash('Access denied...', 'danger')
        return redirect(request.url)
