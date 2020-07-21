import os
from flask import Blueprint
from flask import render_template, request, redirect
from .utils import application_process, add_to_database_all_voters
from dotenv import load_dotenv

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

@form_bp.route('/db/')
def add_to_database():
    add_to_database_all_voters()
    return render_template('formclosed.html')

@form_bp.route('/form/', methods=['POST', 'GET'])
def form():
    if request.method == 'POST':
        if os.environ["FLASK_DEBUG"]:
            application_process(request)
        else:
            try:
                application_process(request)
            except(Exception):
                return redirect('/error/')
        return redirect('/confirmation/')
    else:
        return render_template('form.html')

@form_bp.route('/form/<group>/', methods=['POST', 'GET'])
def form_group(group):
    if request.method == 'POST':
        if os.environ["FLASK_DEBUG"]:
            application_process(request)
        else:
            try:
                application_process(request, group)
            except(Exception):
                return redirect('/error/')
        return redirect('/confirmation/')
    else:
        return render_template('form.html')
