import os
from flask import Blueprint, current_app
from flask import render_template, request, redirect, url_for
from dotenv import load_dotenv
from eAbsentee.app import babel
from eAbsentee.form.utils import application_process
from flask_babel import get_locale

load_dotenv()

form_bp = Blueprint(
    'form_bp',
    __name__,
    template_folder='templates',
    static_folder='static'
)

@form_bp.route('/error/')
def error_page():
    return render_template('error.html')

@form_bp.route('/confirmation/')
def confirmation_page():
    return render_template('confirmation.html')

@form_bp.route('/formclosed/')
def form_closed():
    return render_template('formclosed.html')

@form_bp.route('/longlat/')
def add_to_database():
    add_to_database_long_lat()
    return render_template('formclosed.html')

@form_bp.route('/form/', methods=['POST', 'GET'])
def form():
    lang = get_locale().language
    if current_app.config['FORM_CLOSED']:
        return redirect('/formclosed/')
    if request.method == 'POST':
        if os.environ["FLASK_DEBUG"]:
            application_process(request, lang=lang)
        else:
            try:
                application_process(request, lang=lang)
            except(Exception):
                return redirect('/error/')
        get_parameters = {'lang': lang} if 'lang' in request.args else {}
        return redirect(url_for(f'form_bp.{confirmation_page.__name__}', **get_parameters))
    else:
        return render_template('form.html')


@form_bp.route('/form/<group>/', methods=['POST', 'GET'])
def form_group(group):
    lang = get_locale().language
    if current_app.config['FORM_CLOSED']:
        return redirect('/formclosed/')
    if request.method == 'POST':
        if os.environ["FLASK_DEBUG"]:
            application_process(request, group, lang=lang)
        else:
            try:
                application_process(request, lang=lang)
            except(Exception):
                return redirect('/error/')
        get_parameters = {'lang': lang} if 'lang' in request.args else {}
        return redirect(url_for(f'form_bp.{confirmation_page.__name__}', **get_parameters))
    else:
        return render_template('form.html')
