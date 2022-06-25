# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from werkzeug.datastructures import ImmutableMultiDict

from apps import db
from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound

from apps.home.forms import CreateVCCForm
from apps.home.models import VCC, VCCFormAnswers, VCCSubQuestionsAnswers


@blueprint.route('/index')
@login_required
def index():
    return render_template('home/index.html', segment='index')


@blueprint.route('/vcc-register-answer', methods=['GET', 'POST'])
@login_required
def register_vcc_answer():
    vcc_form = CreateVCCForm()
    print(request.form)
    print(request)
    rere = request

    if request.method == 'POST' and 'vcc_list' in request.form:
        print(request.form)
        if request.form.get('vcc_list') != '':
            vcc_form.hide = 'Block'
            vcc_form.get_questions(int(request.form.get('vcc_list')))
        else:
            vcc_form.hide = 'None'
    elif request.method == 'POST' and 'send_form' in request.form:
        http_args = {'vcc_id': int(request.form.get('send_form').split('_')[0]),
                     'worker_id': int(request.form.get('send_form').split('_')[1]),
                     'observed_area_id': int(request.form.get('areas_list')),
                     'company_id': int(request.form.get('companies_list')), 'event_date': request.form.get('date'),
                     'verified_job': request.form.get('job')}

        vcc_form_answer = VCCFormAnswers(**ImmutableMultiDict(http_args))
        db.session.add(vcc_form_answer)
        db.session.commit()
        sub_answers = request.form.to_dict()
        sub_answers.pop('companies_list')
        sub_answers.pop('date')
        sub_answers.pop('areas_list')
        sub_answers.pop('job')
        sub_answers.pop('send_form')
        keys = sub_answers.keys()
        keys_ids = [item.split('_')[1] for item in keys]
        keys_ids = list(dict.fromkeys(keys_ids))
        print(keys_ids)

        for key_id in keys_ids:
            sub_args = {}
            if 'answer_'+key_id in sub_answers:
                sub_args['vcc_sub_question_id'] = key_id
                sub_args['vcc_form_answer_id'] = vcc_form_answer.id
                sub_args['answer'] = True
                if 'who_'+key_id in request.form:
                    sub_args['workers_id'] = request.form.get('who_'+key_id)
                sub_args['what'] = request.form.get('what_'+key_id)
                sub_args['when'] = request.form.get('when_' + key_id)
                sub_args['state'] = request.form.get('state_' + key_id)
            else:
                sub_args['vcc_sub_question_id'] = key_id
                sub_args['vcc_form_answer_id'] = vcc_form_answer.id
                sub_args['answer'] = False

            vcc_sub_question_answer = VCCSubQuestionsAnswers(**ImmutableMultiDict(sub_args))
            db.session.add(vcc_sub_question_answer)
            db.session.commit()







    return render_template("home/vcc-register-answer.html", form=vcc_form, segment='vcc-register-answer')


@blueprint.route('/<template>')
@login_required
def route_template(template):
    try:

        # if not template.endswith('.html'):
        template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html

        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):
    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500

