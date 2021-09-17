import os
from flask import Blueprint, current_app
from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from dotenv import load_dotenv
from eAbsentee.app import babel
from eAbsentee.form.utils import application_process
from flask_babel import get_locale
# from eAbsentee.app import db
# from eAbsentee.admin.models import GroupReference
# from sqlalchemy.sql import exists

load_dotenv()

form_bp = Blueprint(
    'form',
    __name__,
    template_folder='templates',
    static_folder='static'
)

@form_bp.route('/confirmation/')
def confirmation_page():
    return render_template('confirmation.html')

@form_bp.route('/form/', methods=['POST', 'GET'], defaults={'group': None})
@form_bp.route('/form/<group>/', methods=['POST', 'GET'])
def form(group):
    if current_app.config['FORM_CLOSED']:
        return render_template('formclosed.html')

    if request.method == 'POST':
        lang = get_locale().language
        application_process(request, group_code=group, lang=lang, email_registrar=True)
        get_parameters = {'lang': lang} if 'lang' in request.args else {}
        return redirect(url_for(f'form.{confirmation_page.__name__}', **get_parameters))
    else:
        # if group is not None:
        #     if db.session.query(exists().where(GroupReference.group_code==group)).scalar():
        #         # group does not exist
        #         return redirect('/form/')
        return render_template('form.html')

@form_bp.route('/form-test/', methods=['POST', 'GET'])
@login_required
def form_test():
    if not current_user.is_admin():
        return redirect(url_for('home.index')), 401
    if request.method == 'POST':
        lang = get_locale().language
        application_process(request, lang=lang, email_registrar=False)
        get_parameters = {'lang': lang} if 'lang' in request.args else {}
        return redirect(url_for(f'form.{confirmation_page.__name__}', **get_parameters))
    else:
        return render_template('form.html')

@form_bp.errorhandler(500)
def handle_exception(e):
    return render_template('error.html'), 500
