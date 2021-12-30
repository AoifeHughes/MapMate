from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response
from functools import wraps
import pandas as pd
app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['csv'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_uploaded_file_as_df():
    df = pd.DataFrame()
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        resp = False
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filenameX
    if file.filename == '':
        flash('No selected file')
        resp = False
    if file and allowed_file(file.filename):
        print(file.filename)
        resp = True
        df = pd.read_csv(request.files.get('file'))
    else:
        resp = 'Bad upload file'
    return (resp, df)


@app.route("/", defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def index(path):
    return render_template('index.html')

if __name__ == "__main__":
    app.secret_key = '8080'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='0.0.0.0', port=9666, debug=False)
