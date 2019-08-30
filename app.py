from flask import Flask, render_template, request, redirect, session, send_file
from functions import parse_data, build_pdf, email_registrar
from keys import SECRET_KEY
import os

# Sets CWD to whatever directory app.py is located in
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Initialize flask app, SECRET_KEY can be found in keys.py
app = Flask(__name__)
app.secret_key = SECRET_KEY


# Homepage route
@app.route('/')
def home():
    return render_template('index.html')


''' Form Route: Returns form when requested,
collects data from user when inputted. The data is sent to
functions.py, where it is parsed and converted,
built into the PDF, and emailed to the respective registar. If
unable to send the PDF, an error page is returned. '''

# TODO: Catch specific types of errors, inform that pdf was not sent.
@app.route('/form/', methods=['POST', 'GET'])
def process_form():
    if request.method == 'POST':
        # try:
        email_registrar(
            build_pdf(
                # * unpacks tuple returned by function into arguments
                *parse_data(request)))
        # except(Exception):
        #     return redirect('/error/')
        return redirect('/confirmation/')
    else:
        return render_template('form.html')


# Error Route
@app.route('/error/', methods=['GET'])
def error_page():
    return render_template('formerror.html')


'''Confirmation Route: user is redirected here
after submission of form.
'''

# TODO: Redirect to page based off of succesful submission
@app.route('/confirmation/', methods=['GET'])
def confirmation_page():
    return render_template('confirmation.html')
    # if session.get('output_pdf') is not None:
    #     return render_template('confirmation.html')
    # else:
    #     # TODO: redirect to more appropriate error page (like 403 forbidden)
    #     return redirect('/404/')

# Displays application once submitted to user in .PDF form
@app.route('/applications/<id>.pdf')
def render_pdf(id: str):
    return send_file(
        open(session['output_file'], 'rb'),
        attachment_filename=session['output_file']
    )


# Displays fillable form online
@app.route('/fillableform')
def render_fillableform_pdf():
    return send_file(
        open('static/blankAppFillable.pdf', 'rb'),
        attachment_filename='blankAppFillable.pdf'
    )


# Displays printable form online
@app.route('/printform')
def render_printform_pdf():
    return send_file(
        open('static/blankApp.pdf', 'rb'),
        attachment_filename='blankApp.pdf'
    )


# 404 page route if incorrect url entered
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
