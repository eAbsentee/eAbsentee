from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from functions import buildJSON

app = Flask(__name__, static_url_path='')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/form', methods=['POST', 'GET'])
def process_form():
    if request.method == 'POST':
        buildJSON(request)
        return redirect('confirmation.html')
    else:
        return render_template('form.html')


if __name__ == '__main__':
    app.run(debug=True)
