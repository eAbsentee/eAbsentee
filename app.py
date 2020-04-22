from flask import Flask, render_template, request, redirect, session
from flask import send_file, make_response, send_from_directory
from functions import application_process, add_to_campaign, get_ids_and_counties, email_report_alltime_api
from keys import SECRET_KEY, API_KEY
import os
import time
import datetime

# Sets CWD to whatever directory app.py is located in
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Initialize flask app, SECRET_KEY can be found in keys.py
app = Flask(__name__, template_folder="templates")
app.secret_key = SECRET_KEY
app.root_path = os.path.dirname(os.path.abspath(__file__))
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['DEBUG'] = True
# app.config['EXPLAIN_TEMPLATE_LOADING'] = True


'''Static Routes'''
# Homepage
@app.route('/')
def home():
    return render_template('index.html')


# Error
@app.route('/error/')
def error_page():
    return render_template('formerror.html')


# Credits
@app.route('/credits/', methods=['GET'])
def credits_page():
    return render_template('credits.html')

# List of Counties for API
@app.route('/listcounty/')
def list_of_counties():
    return(render_template('list_of_counties.html'))


# About
@app.route('/about/')
def about():
    return(render_template('about.html'))


@app.route('/confirmation/')
def confirmation_page():
    """Confirmation Route: user is redirected here after submission of form. """
    return render_template('confirmation.html')


@app.route('/formclosed/')
def form_closed():
    return render_template("formclosed.html")


@app.route('/hb1/')
def hb1():
    return render_template("hb1.html")

# Bills

# @app.route('/hb201/')
# def hb201():
#     return render_template("hb201.html")
#
#
# @app.route('/hb207/')
# def hb207():
#     return render_template("hb207.html")
#
#
# @app.route('/hb220/')
# def hb220():
#     return render_template("hb220.html")
#
#
# @app.route('/hb238/')
# def hb238():
#     return render_template("hb238.html")


'''Static PDF Routes'''
# Fillable Form as .PDF
@app.route('/fillableform/')
def render_fillableform_pdf():
    return send_file(
        open('static/pdf/blank_app_fillable.pdf', 'rb'), attachment_filename='blank_app_fillable.pdf'
    )

# Printable Form as .PDF
@app.route('/printform/')
def render_printform_pdf():
    return send_file(
        open('static/pdf/blank_app_printable.pdf', 'rb'), attachment_filename='blank_app_printable.pdf'
    )


@app.route('/videocredits/')
def render_videocredits_pdf():
    return send_file(
        open('static/pdf/credits.pdf', 'rb'), attachment_filename='credits.pdf'
    )


@app.route('/applications/<id>.pdf')
def render_pdf(id):
    '''Displays application to user in PDF form'''
    return send_file(
        open(session['output_file'], 'rb'), attachment_filename=session['output_file']
    )

@app.route('/privacy/')
def privacy():
    return send_file(
        open('static/pdf/privacy_policy.pdf', 'rb'), attachment_filename='privacy_policy.pdf'
    )

# 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


''' FORM ROUTES '''


@app.route('/form/', methods=['POST', 'GET'])
def process_form():
    """ Form Route: Returns form when requested, collects data from user when inputted. The data is sent to
    functions.py, where it is parsed and converted, built into the PDF, and emailed to the respective registar. If
    unable to send the PDF, an error page is returned. """
    if request.method == 'POST':
        # try:
        application_process(request)
        # except(Exception):
            # return redirect('/error/')
        return redirect('/confirmation/')
    else:
        # return render_template('formclosed.html')
        ids_and_counties = get_ids_and_counties('allcounties')
        if 'campaign' in request.cookies:
            ids_and_counties = get_ids_and_counties(
                request.cookies.get('campaign'))
        return render_template('form.html', ids_and_counties=ids_and_counties)


@app.route('/form/<group>/', methods=['POST', 'GET'])
def form_group(group: str):
    if request.method == 'POST':
        try:
            application_process(request, group)
        except(Exception):
            return redirect('/error/')
        return redirect('/confirmation/')
    else:
        if group == 'fcdc':
            return render_template('form_fcdc.html', ids_and_counties=get_ids_and_counties('fcdc'))
        return render_template('form.html', ids_and_counties=get_ids_and_counties('allcounties'))


@app.route('/formdev/', methods=['POST', 'GET'])
def form_dev():
    if request.method == 'POST':
        application_process(request)
        return redirect('/confirmation/')
    else:
        ids_and_counties = get_ids_and_counties('dagaprez')
        return render_template('form.html', ids_and_counties=ids_and_counties)


''' COOKIE ROUTES '''


@app.route('/c/<campaign>')
def home_with_campaign(campaign: str):
    """This route sets the county cookies. It is used to determine which form
    to display. The different forms can have different counties displayed."""
    response = make_response(redirect('/'))
    response.set_cookie('campaign', campaign, max_age=60 * 60 * 24 * 365)
    return response


@app.route('/g/<group>')
def set_group(group: str):
    """This route sets the group cookies."""
    response = make_response(redirect('/'))
    response.set_cookie('group', group, max_age=60 * 60 * 24 * 365)
    return response


''' API ROUTES '''


@app.route('/api/', methods=['POST', 'GET'])
def api():
    if request.method == 'POST':
        if request.form.get('group_name') or request.form.get('campaign_name'):
            add_to_campaign(request)
            return render_template('api.html')
        elif request.form.get('email_spreadsheet'):
            if request.form.get('api_key') == API_KEY:
                email_report_alltime_api(request)
            return render_template('api.html')
        return render_template('api.html')
    else:
        return render_template('api.html')


''' FAVICONS '''


@app.route('/apple-touch-icon.png', methods=['GET'])
def apple_touch_icon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicons/apple-touch-icon.png',
                               mimetype='image/png')


@app.route('/android-chrome-192x192.png', methods=['GET'])
def android_chrome_192x192():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicons/android-chrome-192x192.png',
                               mimetype='image/png')


@app.route('/android-chrome-512x512.png', methods=['GET'])
def android_chrome_512x512():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicons/android-chrome-512x512.png',
                               mimetype='image/png')


@app.route('/mstile-70x70.png', methods=['GET'])
def mstile_70x70():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicons/mstile-70x70.png',
                               mimetype='image/png')


@app.route('/mstile-144x144.png', methods=['GET'])
def mstile_144x144():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicons/mstile-144x144.png',
                               mimetype='image/png')


@app.route('/mstile-150x150.png', methods=['GET'])
def mstile_150x150():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicons/mstile-150x150.png',
                               mimetype='image/png')


@app.route('/mstile-310x150.png', methods=['GET'])
def mstile_310x150():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicons/mstile-310x150.png',
                               mimetype='image/png')


@app.route('/mstile-310x310.png', methods=['GET'])
def mstile_310x310():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicons/mstile-310x310.png',
                               mimetype='image/png')


@app.route('/safari-pinned-tab.svg', methods=['GET'])
def safar_pinned_tab():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicons/safari-pinned-tab.svg',
                               mimetype='image/png')


@app.route('/favicon.ico', methods=['GET'])
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicons/favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@app.route('/favicon-16x16.png', methods=['GET'])
def favicon_16x16():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicons/favicon-16x16.png',
                               mimetype='image/png')


@app.route('/favicon-32x32.png', methods=['GET'])
def favicon_32x32():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicons/favicon-32x32.png',
                               mimetype='image/png')


if __name__ == '__main__':
    app.run()
