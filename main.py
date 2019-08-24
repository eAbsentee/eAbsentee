from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from functions import parse_data

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/form/', methods=['POST', 'GET'])
def process_form():
    if request.method == 'POST':
        parse_data(request)
        return redirect('/confirmation/')
    else:
        return render_template('form.html')


@app.route('/confirmation/', methods=['GET'])
def confirmation():
    return render_template('confirmation.html')


if __name__ == '__main__':
    app.run(debug=True)
