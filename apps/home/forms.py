
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import Email, DataRequired


from apps.home.models import VCC, VCCQuestions, Companies, Areas


class CreateVCCForm(FlaskForm):
    title = 'Seleccione un VCC'
    hide = 'None'
    area = ''
    vcc = None
    questions = []
    vcc_list = SelectField()
    companies_list = SelectField()
    areas_list = SelectField()
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
        self.questions = [(c.id, c.code, c.question) for c in VCCQuestions.query.filter_by(time_elimination=None, vcc_id=vcc_id)]

