import os
from flask import Blueprint
from flask import render_template, send_file, send_from_directory, make_response

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



@home_bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@home_bp.route('/apple-touch-icon.png', methods=['GET'])
def apple_touch_icon():
    return send_from_directory(os.path.join('..', 'static'),
                               'favicons/apple-touch-icon.png',
                               mimetype='image/png')


@home_bp.route('/android-chrome-192x192.png', methods=['GET'])
def android_chrome_192x192():
    return send_from_directory(os.path.join('..', 'static'),
                               'favicons/android-chrome-192x192.png',
                               mimetype='image/png')


@home_bp.route('/android-chrome-512x512.png', methods=['GET'])
def android_chrome_512x512():
    return send_from_directory(os.path.join('..', 'static'),
                               'favicons/android-chrome-512x512.png',
                               mimetype='image/png')


@home_bp.route('/mstile-70x70.png', methods=['GET'])
def mstile_70x70():
    return send_from_directory(os.path.join('..', 'static'),
                               'favicons/mstile-70x70.png',
                               mimetype='image/png')


@home_bp.route('/mstile-144x144.png', methods=['GET'])
def mstile_144x144():
    return send_from_directory(os.path.join('..', 'static'),
                               'favicons/mstile-144x144.png',
                               mimetype='image/png')


@home_bp.route('/mstile-150x150.png', methods=['GET'])
def mstile_150x150():
    return send_from_directory(os.path.join('..', 'static'),
                               'favicons/mstile-150x150.png',
                               mimetype='image/png')


@home_bp.route('/mstile-310x150.png', methods=['GET'])
def mstile_310x150():
    return send_from_directory(os.path.join('..', 'static'),
                               'favicons/mstile-310x150.png',
                               mimetype='image/png')


@home_bp.route('/mstile-310x310.png', methods=['GET'])
def mstile_310x310():
    return send_from_directory(os.path.join('..', 'static'),
                               'favicons/mstile-310x310.png',
                               mimetype='image/png')


@home_bp.route('/safari-pinned-tab.svg', methods=['GET'])
def safar_pinned_tab():
    return send_from_directory(os.path.join('..', 'static'),
                               'favicons/safari-pinned-tab.svg',
                               mimetype='image/png')


@home_bp.route('/favicon.ico', methods=['GET'])
def favicon():
    return send_from_directory(os.path.join('..', 'static'),
                               'favicons/favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@home_bp.route('/favicon-16x16.png', methods=['GET'])
def favicon_16x16():
    return send_from_directory(os.path.join('..', 'static'),
                               'favicons/favicon-16x16.png',
                               mimetype='image/png')


@home_bp.route('/favicon-32x32.png', methods=['GET'])
def favicon_32x32():
    return send_from_directory(os.path.join('..', 'static'),
                               'favicons/favicon-32x32.png',
                               mimetype='image/png')
