from flask import Flask, render_template, request, redirect, session, send_file
from functions import parse_data, build_pdf, email_registrar
from keys import SECRET_KEY
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
app.secret_key = SECRET_KEY


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/form/', methods=['POST', 'GET'])
def process_form():
    if request.method == 'POST':
        email_registrar(
            build_pdf(
                # Asterisk unpacks tuple returned by function into arguments.
                *parse_data(request)))
        return redirect('/confirmation/')
    else:
        return render_template('form.html')


@app.route('/confirmation/', methods=['GET'])
def confirmation():
    if session.get('output_pdf') is not None:
        return render_template('confirmation.html')
    else:
        # TODO: redirect to more appropriate error page (like 403 forbidden)
        return redirect('/404/')


@app.route('/applications/<id>.pdf')
def render_pdf(id: str):
    return send_file(
        open(session['output_file'], 'rb'),
        attachment_filename=session['output_file']
    )


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
