from sqlalchemy import func
from sqlalchemy.dialects import postgresql as pg

from apps import db


class Workers(db.Model):
    __tablename__ = 'tb_workers'
    id = db.Column("id", db.Integer, primary_key=True, nullable=False)
    names = db.Column("names", db.Text, nullable=False)
    first_surname = db.Column("first_surname", db.Text, nullable=False)
    second_surname = db.Column("second_surname", db.Text, nullable=False)
    email = db.Column("email", db.Text)
    phone = db.Column("phone", db.Text)
    gender = db.Column("gender", db.Integer, nullable=False)
    document_type = db.Column("document_type", db.Integer, nullable=False)
    date_birth = db.Column("date_birth", db.Date, nullable=False)
    company_id = db.Column("company_id", db.Integer, nullable=False)
    area_1_id = db.Column("area_1_id", db.Integer, nullable=False)
    area_2_id = db.Column("area_2_id", db.Integer)
    job_title = db.Column("job_title", db.Text, nullable=False)
    time_creation = db.Column("time_creation", db.TIMESTAMP, default=func.now(), nullable=False)
    time_elimination = db.Column("time_elimination", db.TIMESTAMP, nullable=True)

    def __int__(self, **kwargs):
        for property, value in kwargs.items():
            setattr(self, property, value)


class Areas(db.Model):
    __tablename__ = 'tb_areas'
    id = db.Column("id", db.Integer, primary_key=True, nullable=False)
    area = db.Column("area", db.Text, nullable=False)
    time_creation = db.Column("time_creation", db.TIMESTAMP, default=func.now(), nullable=False)
    time_elimination = db.Column("time_elimination", db.TIMESTAMP, nullable=True)

    def __int__(self, **kwargs):
        for property, value in kwargs.items():
            setattr(self, property, value)


class Companies(db.Model):
    __tablename__ = 'tb_companies'
    id = db.Column("id", db.Integer, primary_key=True, nullable=False)
    company = db.Column("company", db.Text, nullable=False)
    ruc = db.Column("ruc", db.Text, nullable=False)
    time_creation = db.Column("time_creation", db.TIMESTAMP, default=func.now(), nullable=False)
    time_elimination = db.Column("time_elimination", db.TIMESTAMP, nullable=True)

    def __int__(self, **kwargs):
        for property, value in kwargs.items():
            setattr(self, property, value)


class VCC(db.Model):
    __tablename__ = 'tb_vcc'
    id = db.Column("id", db.Integer, primary_key=True, nullable=False)
    name = db.Column("name", db.Text, nullable=False)
    code = db.Column("code", db.Text, nullable=False)
    version = db.Column("version", db.Text, nullable=False)
    elaboration_date = db.Column("elaboration_date", db.Date, nullable=False)
    time_creation = db.Column("time_creation", db.TIMESTAMP, default=func.now(), nullable=False)
    time_elimination = db.Column("time_elimination", db.TIMESTAMP, nullable=True)

    def __int__(self, **kwargs):
        for property, value in kwargs.items():
            setattr(self, property, value)

    def __repr__(self):
        return "<VCC(id='%s', name='%s')>" % (self.id, self.name)


class VCCFormAnswers(db.Model):
    __tablename__ = 'tb_vcc_form_answers'
    id = db.Column("id", db.Integer, primary_key=True, nullable=False)
    vcc_id = db.Column("vcc_id", db.Integer, nullable=False)
    worker_id = db.Column("worker_id", db.Integer, nullable=False)
    observed_area_id = db.Column("observed_area_id", db.Integer, nullable=False)
    company_id = db.Column("company_id", db.Integer, nullable=False)
    event_date = db.Column("event_date", db.Date, nullable=False)
    verified_job = db.Column("verified_job", db.Text, nullable=False)
    time_creation = db.Column("time_creation", db.TIMESTAMP, default=func.now(), nullable=False)
    time_elimination = db.Column("time_elimination", db.TIMESTAMP, nullable=True)

    def __int__(self, **kwargs):
        for property, value in kwargs.items():
            setattr(self, property, value)


class VCCQuestions(db.Model):
    __tablename__ = 'tb_vcc_questions'
    id = db.Column("id", db.Integer, primary_key=True, nullable=False)
    vcc_id = db.Column("vcc_id", db.Integer, nullable=False)
    code = db.Column("code", db.Text, nullable=False)
    question = db.Column("question", db.Text, nullable=False)
    time_creation = db.Column("time_creation", db.TIMESTAMP, default=func.now(), nullable=False)
    time_elimination = db.Column("time_elimination", db.TIMESTAMP, nullable=True)

    def __int__(self, **kwargs):
        for property, value in kwargs.items():
            setattr(self, property, value)


class VCCSubQuestions(db.Model):
    __tablename__ = 'tb_vcc_sub_questions'
    id = db.Column("id", db.Integer, primary_key=True, nullable=False)
    vcc_question_id = db.Column("vcc_question_id", db.Integer, nullable=False)
    code = db.Column("code", db.Text, nullable=False)
    sub_question = db.Column("sub_question", db.Text, nullable=False)
    time_creation = db.Column("time_creation", db.TIMESTAMP, default=func.now(), nullable=False)
    time_elimination = db.Column("time_elimination", db.TIMESTAMP, nullable=True)

    def __int__(self, **kwargs):
        for property, value in kwargs.items():
            setattr(self, property, value)


class VCCSubQuestionsAnswers(db.Model):
    __tablename__ = 'tb_vcc_sub_questions_answers'
    id = db.Column("id", db.Integer, primary_key=True, nullable=False)
    vcc_sub_question_id = db.Column("vcc_sub_question_id", db.Integer, nullable=False)
    vcc_form_answer_id = db.Column("vcc_form_answer_id", db.Integer, nullable=False)
    workers_id = db.Column("workers_id", pg.ARRAY(db.Integer, dimensions=1), nullable=False)
    what = db.Column("what", db.Text, nullable=False)
    when = db.Column("when", db.TIMESTAMP, nullable=False)
    state = db.Column("state", db.Text, nullable=False)
    time_creation = db.Column("time_creation", db.TIMESTAMP, default=func.now(), nullable=False)
    time_elimination = db.Column("time_elimination", db.TIMESTAMP, nullable=True)

    def __int__(self, **kwargs):
        for property, value in kwargs.items():
            setattr(self, property, value)
