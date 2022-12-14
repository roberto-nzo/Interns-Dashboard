from datetime import datetime
from .extensions import db, ModelView
from flask import session, flash
from flask import abort, redirect, url_for


class User(db.Model):
    studentnumber = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    major = db.Column(db.String(100), nullable=False)
    degree = db.Column(db.String(100), nullable=False)
    register_date = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    studentmail = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.surname


class Dashboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topics = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    startingdate = db.Column(db.Date, nullable=False)
    finishdate = db.Column(db.Date, nullable=False)

    studentnumber = db.Column(db.Integer, db.ForeignKey(
        'user.studentnumber'), nullable=False)
    user = db.relationship('User', backref=db.backref(
        'users_dashboard', lazy=True))

    def __repr__(self):
        return '<Dashboard %r>' % self.topics


class Topic_create(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topics = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    startingdate = db.Column(db.Date, nullable=False)
    finishdate = db.Column(db.Date, nullable=False)

    studentnumber = db.Column(db.Integer, db.ForeignKey(
        'user.studentnumber'), nullable=False)
    user = db.relationship('User', backref=db.backref(
        'users_topic_create', lazy=True))

    def __repr__(self):
        return '<Topic_create %r>' % self.topics


class appr_disappr(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    studentnumber = db.Column(db.Integer, db.ForeignKey(
        'topic_create.studentnumber'), nullable=False)
    topics = db.Column(db.String(250), db.ForeignKey(
        'topic_create.topics'), nullable=False)
    id_topic = db.Column(db.Integer, db.ForeignKey(
        'topic_create.id'), nullable=False)
    description = db.Column(db.String(500), db.ForeignKey(
        'topic_create.description'), nullable=False)
    startingdate = db.Column(db.Date, db.ForeignKey(
        'topic_create.startingdate'), nullable=False)
    finishdate = db.Column(db.Date, db.ForeignKey(
        'topic_create.finishdate'), nullable=False)

    def __repr__(self):
        return '<appr_disappr> %r' % self.topics


class SecureModelView(ModelView):
    def is_accessible(self):
        if session:
            if session['studentnumber'] == 1:
                return True
            else:
                abort(403)
        else:
            abort(403)
