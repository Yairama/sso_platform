# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound

from apps.home.forms import CreateVCCForm
from apps.home.models import VCC


@blueprint.route('/index')
@login_required
def index():
    return render_template('home/index.html', segment='index')


@blueprint.route('/vcc-register-answer', methods=['GET', 'POST'])
@login_required
def register_vcc_answer():
    vcc_form = CreateVCCForm()
    print(request.form)

    if request.method == 'POST':
        if request.form.get('vcc_list') != '':
            vcc_form.hide = 'Block'
            vcc_form.get_questions(int(request.form.get('vcc_list')))
            print(vcc_form.questions)
        else:
            vcc_form.hide = 'None'

        print()

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
