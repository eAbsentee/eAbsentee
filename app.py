from flask import Flask, render_template, request, redirect, session
from flask import send_file, make_response, send_from_directory
from functions import application_process, add_to_groups, get_ids_and_counties, email_report_alltime_api
from fcdc_functions import add_group
from keys import SECRET_KEY, API_KEY, API_KEY_FCDC
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

"""Home Route"""
@app.route('/')
def home():
    return render_template('index.html')

"""Form Error Route: users are directed here if an error is encountered during the processing of their application"""
@app.route('/error/')
def error_page():
    return render_template('formerror.html')

"""Credits Route: credits for the template, developers, and team behind the website"""
@app.route('/credits/', methods=['GET'])
def credits_page():
    return render_template('credits.html')

"""List of Counties Route: displays all counties and their matching numerical ID as information for the API"""
@app.route('/listcounty/')
def list_of_counties():
    return(render_template('list_of_counties.html'))

"""About Route: displays information about eAbsentee and Vote Absentee Virginia."""
@app.route('/about/')
def about():
    return(render_template('about.html'))


"""Confirmation Route: user is redirected here after submission of form. """
@app.route('/confirmation/')
def confirmation_page():
    return render_template('confirmation.html')

"""Form Closed Route: user is redirected here from the form route when absentee ballot applications are no longer being accepted."""
@app.route('/formclosed/')
def form_closed():
    return render_template("formclosed.html")


"""Static PDF Routes"""

"""Fillable Form"""
@app.route('/fillableform/')
def render_fillableform_pdf():
    return send_file(
        open('static/pdf/blank_app_fillable.pdf', 'rb'), attachment_filename='blank_app_fillable.pdf'
    )

"""Printable Form"""
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


"""Displays application using session variables set in functions.py"""
@app.route('/applications/<id>.pdf')
def render_pdf(id):
    return send_file(
        open(session['output_file'], 'rb'), attachment_filename=session['output_file']
    )

@app.route('/privacy/')
def privacy():
    return send_file(
        open('static/pdf/privacy_policy.pdf', 'rb'), attachment_filename='privacy_policy.pdf'
    )

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


''' FORM ROUTES '''
@app.route('/form/', methods=['POST', 'GET'])
def form():
    """ Form Route: Returns form when requested, collects data from user when inputted. The data is sent to functions.py, where it is parsed and converted, built into the PDF, and emailed to the respective registar. If
    unable to send the PDF, an error page is returned. """
    if request.method == 'POST':
        try:
            application_process(request)
        except(Exception):
            return redirect('/error/')
        return redirect('/confirmation/')
    else:
        if 'group' in request.cookies:
            ids_and_counties = get_ids_and_counties(request.cookies.get('group'))
            return render_template('form.html', ids_and_counties=ids_and_counties)
        else:
            ids_and_counties = get_ids_and_counties('allcounties')
            return render_template('form.html', ids_and_counties=ids_and_counties)


@app.route('/form/<group>/', methods=['POST', 'GET'])
def form_group(group):
    if request.method == 'POST':
        try:
            application_process(request, group)
        except(Exception):
            return redirect('/error/')
        return redirect('/confirmation/')
    else:
        return render_template('form.html', ids_and_counties=get_ids_and_counties(group))



''' COOKIE ROUTES '''
@app.route('/g/<group>/')
def set_group(group: str):
    """This route sets the group cookies."""
    response = make_response(redirect('/'))
    response.set_cookie('group', group, max_age=60 * 60 * 24 * 365)
    return response

''' API ROUTES '''
@app.route('/api/', methods=['POST', 'GET'])
def api():
    if request.method == 'POST':
        if request.form.get('group_code'):
            add_to_groups(request)
            return render_template('api.html')
        elif request.form.get('email_spreadsheet'):
            email_report_alltime_api(request)
            return render_template('api.html')
        return render_template('api.html')
    else:
        return render_template('api.html')

@app.route('/api_fcdc/', methods=['POST', 'GET'])
def api_fcdc():
    if request.method == 'POST':
        add_group(request)
        return render_template('api_fcdc.html')
    else:
        return render_template('api_fcdc.html')


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
