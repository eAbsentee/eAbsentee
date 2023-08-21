import os
from flask import Blueprint, current_app
from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from dotenv import load_dotenv
from eAbsentee.app import babel
from eAbsentee.form.utils import application_process, SystemOverloadError
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

@form_bp.route('/form/', methods=['POST', 'GET'], defaults={'group': None})
@form_bp.route('/form/<group>/', methods=['POST', 'GET'])
def form(group):
    if not current_app.config['FORM_OPEN']:
        return render_template('formclosed.html')

    if request.method == 'POST':
        lang = get_locale().language
        application_process(request, group_code=group, lang=lang, email_registrar=True)
        return render_template('confirmation.html')
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
        return render_template('confirmation.html')
    else:
        return render_template('form.html')

@form_bp.errorhandler(SystemOverloadError)
def handle_system_overload(e):
    # Here, we can return an error page with JavaScript to automatically retry the form submission after 5 seconds
    # This is a placeholder and can be replaced with the actual error page name.
    return render_template('system_overload_error.html'), 500
@form_bp.errorhandler(500)
def handle_exception(e):
    return render_template('error.html'), 500
