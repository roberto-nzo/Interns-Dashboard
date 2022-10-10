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
        results = Topic_create.query.filter(User.studentnumber!=1).all()
        m = []
        for x in results:
            if x.studentnumber not in m:
                m.append(x.studentnumber)
        print(m)
        return render_template('studentsdashboard.html', outputs=outputs, m=m)
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

        disaprove = appr_disappr.query.filter_by(studentnumber=studentnumber).all()
        list_disaprove = []
        for l in disaprove:
            if l.id_topic not in list_disaprove:
                list_disaprove.append(l.id_topic)
        
        # Display dashboard graph of the student
        datas_dict = {"id": [], "topics":[], "description":[], "startingdate":[], "finishdate": []}
        if outputs:
            for x in outputs:
                datas_dict['id'].append(x.id)
                datas_dict["topics"].append(x.topics)
                datas_dict['description'].append(x.description)
                datas_dict['startingdate'].append(x.startingdate)
                datas_dict['finishdate'].append(x.finishdate)
            
            df = pd.DataFrame(datas_dict)
            df['duration'] = df['finishdate'] - df['startingdate']
            df['days'] = df['duration'].dt.days
            df['done'] = datetime.today().date() - df['startingdate']
            df['complete'] = df['done'].dt.days
            df['percentages'] = (df['complete']*100)/df['days']
            for p in df['percentages']:
                if p > 100.0:
                    df['percentages'] = df['percentages'].replace([p], 100)

            print()
            print(df)
            fig1 = px.timeline(df, x_start='startingdate', x_end='finishdate', y='id', color='percentages', hover_name='topics')
            fig1.update_yaxes(autorange='reversed')
            graph1json = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
            
            return render_template('approvedisapprove.html', user=user, outputs=outputs, results=results, list_disaprove=list_disaprove, graph1json=graph1json)
        
        else:
            return render_template('approvedisapprove.html', user=user, outputs=outputs, results=results, list_disaprove=list_disaprove)
    else:
        flash('Access denied...', 'danger')
        return redirect(url_for("main.home"))

# Move rows to another table
@admin.route('/approve/<id>/<studentnumber>/<topics>')
@login_required
def approve(studentnumber, topics, id):
    if session['studentnumber'] == 1:
        topic = Topic_create.query.filter_by(id=id).first_or_404()
        dash = Dashboard(studentnumber=topic.studentnumber, topics=topic.topics, description=topic.description, startingdate=topic.startingdate, finishdate=topic.finishdate)
        db.session.add(dash)
        db.session.delete(topic)
        db.session.commit()
        disaprove = appr_disappr.query.filter_by(id_topic=topic.id).first()
        print(disaprove)
        if disaprove:
            db.session.delete(disaprove)
            db.session.commit()
        else:
            pass

        return redirect(url_for('admin.approvedisapprove', studentnumber=studentnumber))
    else:
        flash('Access denied...', 'danger')
        return redirect(request.url)

@admin.route('/disapprove/<id>/<studentnumber>/<topics>')
@login_required
def disapprove(studentnumber, topics, id):
    if session['studentnumber'] == 1:
        topic = Topic_create.query.filter_by(id=id).first_or_404()
        disapprove = appr_disappr(id_topic = topic.id, studentnumber=topic.studentnumber, topics=topic.topics, description=topic.description, startingdate=topic.startingdate, finishdate=topic.finishdate)
        db.session.add(disapprove)
        db.session.commit()

        return redirect(url_for('admin.approvedisapprove', studentnumber=studentnumber))

    else:
        flash('Access denied...', 'danger')
        return redirect(request.url)