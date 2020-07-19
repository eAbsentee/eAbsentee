from flask import Blueprint
from flask import render_template, request, make_response
from .utils import add_to_groups, email_report_alltime_api, add_group_fcdc
from ..form.models import User

admin_bp = Blueprint(
    'admin_bp',
    __name__,
    template_folder='templates',
    static_folder='static'
)

''' Cookie Routes '''
@admin_bp.route('/g/<group>/')
def set_group(group: str):
    response = make_response(render_template('index.html'))
    response.set_cookie('group', group, max_age=60 * 60 * 24 * 365)
    return response

@admin_bp.route('/admin/interface/')
def admin_interface():
    return render_template(
        'interface.html',
        users=User.query.all()
    )

''' API ROUTES '''
@admin_bp.route('/api/', methods=['POST', 'GET'])
def api():
    if request.method == 'POST':
        if request.form.get('group_code'):
            add_to_groups(request)
        elif request.form.get('email_spreadsheet'):
            email_report_alltime_api(request)
        return render_template('api.html')
    else:
        return render_template('api.html')

@admin_bp.route('/api_fcdc/', methods=['POST', 'GET'])
def api_fcdc():
    if request.method == 'POST':
        add_group(request)
        return render_template('api_fcdc.html')
    else:
        return render_template('api_fcdc.html')
