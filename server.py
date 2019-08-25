from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from functions import parse_data, build_pdf, email_registrar
from os import getenv
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/form/', methods=['POST', 'GET'])
def process_form():
    if request.method == 'POST':
        email_registrar(build_pdf(parse_data(request)))
        return redirect('/confirmation/')
    else:
        return render_template('form.html')


@app.route('/confirmation/', methods=['GET'])
def confirmation():
    return render_template('confirmation.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=(getenv("DEBUG", "FALSE").upper() == "TRUE"))
