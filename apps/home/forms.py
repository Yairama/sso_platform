
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, BooleanField, Form
from wtforms.validators import Email, DataRequired


from apps.home.models import VCC, VCCQuestions, Companies, Areas, VCCSubQuestions, Workers


class CreateVCCForm(FlaskForm):
    title = 'Seleccione un VCC'
    hide = 'None'
    date = DateField(format='%d/%m/%y', validators=[DataRequired()])
    vcc = None
    questions = []
    sub_questions = {}
    vcc_list = SelectField()
    companies_list = SelectField(validators=[DataRequired()])
    areas_list = SelectField(validators=[DataRequired()])
    job = StringField(validators=[DataRequired()])

    def __init__(self):
        super(CreateVCCForm, self).__init__()
        self.vcc_list.choices = [(c.id, c.name) for c in VCC.query.filter_by(time_elimination=None)]
        self.vcc_list.choices.insert(0,("", "---"))
        self.companies_list.choices = [(c.id, c.company) for c in Companies.query.filter_by(time_elimination=None)]
        self.companies_list.choices.insert(0,("", "---"))
        self.areas_list.choices = [(c.id, c.area) for c in Areas.query.filter_by(time_elimination=None)]
        self.areas_list.choices.insert(0,("", "---"))

    def get_questions(self, vcc_id):
        self.vcc = VCC.query.filter_by(time_elimination=None, id=vcc_id).first()
        self.title = 'Código: ' + self.vcc.code + '\n' + 'Version: ' + self.vcc.version
        self.questions = []
        self.questions = [(c.id, c.code, c.question) for c in VCCQuestions.query.filter_by(time_elimination=None,
                                                                                           vcc_id=vcc_id)]
        self.sub_questions = {}
        for id, code, question in self.questions:
            subs = [CreateVCCSubForm(c.id, c.code, c.sub_question) for c in VCCSubQuestions.query.filter_by(time_elimination=None, vcc_question_id=id)]
            self.sub_questions[id] = subs


class CreateVCCSubForm(FlaskForm):

    id = 0
    code = ''
    sub_question = ''
    hide = 'None'
    answer = False
    what = StringField()
    who = SelectField()
    when = DateField(format='%d/%m/%y')
    state = StringField()

    def __init__(self, id, code, sub_question):
        super(CreateVCCSubForm, self).__init__()
        self.id = id
        self.code = code
        self.sub_question = sub_question
        self.what.id = f'what_{self.id}'
        self.what.name = f'what_{self.id}'
        self.who.id = f'who_{self.id}'
        self.who.name = f'who_{self.id}'
        self.when.id = f'when_{self.id}'
        self.when.name = f'when_{self.id}'
        self.state.id = f'state_{self.id}'
        self.state.name = f'state_{self.id}'
        self.who.choices = [(c.id, f'{c.names} {c.first_surname} {c.second_surname}') for c in Workers.query.filter_by(time_elimination=None)]


