# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin
from sqlalchemy.sql.functions import func

from apps import db, login_manager

from apps.authentication.util import hash_pass
from apps.home.models import Workers


class Users(db.Model, UserMixin):
    __tablename__ = 'tb_users'

    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column("user", db.Text)
    email = db.Column("email", db.Text)
    level = db.Column("level", db.Integer)
    worker_id = db.Column("worker_id", db.Integer)
    time_creation = db.Column("time_creation", db.TIMESTAMP, default=func.now())
    time_elimination = db.Column("time_elimination", db.TIMESTAMP, nullable=True)
    password = db.Column(db.LargeBinary)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            if property == 'document':
                setattr(self, 'worker_id', value)
                continue

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)

    def get_worker(self):
        worker = Workers.query.filter_by(time_elimination=None, id=self.worker_id).first()
        return worker


@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id, time_elimination=None).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    return user if user else None


