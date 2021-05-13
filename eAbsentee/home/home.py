import os
from flask import Blueprint
from flask import render_template, send_file, make_response
from flask import current_app

home_bp = Blueprint(
    'home_bp',
    __name__,
    template_folder='templates',
    static_folder='static'
)

@home_bp.route('/')
@home_bp.route('/home/')
def home():
    return render_template('index.html')

@home_bp.route('/credits/', methods=['GET'])
def credits_page():
    return render_template('credits.html')

@home_bp.route('/about/')
def about():
    return(render_template('about.html'))

@home_bp.route('/privacy/')
def privacy():
    return send_file('./static/pdf/privacy_policy.pdf', attachment_filename='privacy_policy.pdf')

@home_bp.route('/g/<group>/')
def set_group(group: str):
    response = make_response(render_template('index.html'))
    response.set_cookie('group', group.lower(), max_age=60 * 60 * 24 * 365)
    return response

@home_bp.route('/2020vote/')
def set_group_2020():
    response = make_response(render_template('index.html'))
    response.set_cookie('group', '2020vote', max_age=60 * 60 * 24 * 365)
    return response

@home_bp.route('/2020Vote/')
def set_group_2020_caps():
    response = make_response(render_template('index.html'))
    response.set_cookie('group', '2020vote', max_age=60 * 60 * 24 * 365)
    return response

@home_bp.route('/2020vote/')
def set_group_2020_vote_lowercase():
    response = make_response(render_template('index.html'))
    response.set_cookie('group', '2020vote', max_age=60 * 60 * 24 * 365)
    return response

@home_bp.route('/AllVote2020/')
def set_group_allvote2020():
    response = make_response(render_template('index.html'))
    response.set_cookie('group', 'AllVote2020', max_age=60 * 60 * 24 * 365)
    return response

@home_bp.route('/site.webmanifest')
def web_app_manifest():
    return current_app.send_static_file('favicon/site.webmanifest')

@home_bp.route('/browserconfig.xml')
def browserconfig_xml():
    return current_app.send_static_file('favicon/browserconfig.xml')

@home_bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
