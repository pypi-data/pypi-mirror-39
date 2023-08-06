import os

from dlpipeline.demo.web_app.app.config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from dlpipeline.demo.web_app.app.models.model import run_model
from dlpipeline.demo.web_app.app.routes import uploads
from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

# A <form> tag is marked with enctype=multipart/form-data and an <input type=file> is placed in that form.
# The application accesses the file from the files dictionary on the request object.
# use the save() method of the file to save the file permanently somewhere on the filesystem.


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', UPLOAD_FOLDER)
app.config['MAX_CONTENT_LENGTH'] = os.getenv('MAX_CONTENT_LENGTH', 10 * 1024 * 1024)  # max upload - 10MB
app.secret_key = os.getenv('SECRET_KEY', 'oh_so_secret')

app.register_blueprint(uploads.uploads)


@app.route('/')
def home():
  return render_template('index.html',
                         result=None)


@app.errorhandler(404)
def url_error(e):
  return (f'''
    Wrong URL!
    <pre>{e}</pre>''', 404)


@app.errorhandler(500)
def server_error(e):
  return (f'''
    An internal error occurred: <pre>{e}</pre>
    See logs for full stacktrace.
    ''', 500)


def allowed_file(filename):
  '''
  check if an extension is valid and that uploads the file and redirects the user to the URL for the
  uploaded file

  :param filename:
  :return:
  '''
  return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/assessment')
def assess_input():
  return render_template('index.html',
                         result=None,
                         scroll='third')


@app.route('/assessment', methods=['GET', 'POST'])
def upload_and_classify():
  if request.method == 'POST':

    # check if the post request has the file part
    if 'file' not in request.files:
      flash('No file part')
      return redirect(url_for('assess_input'))

    file = request.files['file']

    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
      flash('No selected file')
      return redirect(url_for('assess_input'))

    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)

      file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
      file.save(file_path)

      model_results = run_model(file_path)

      return render_template('results.html', result=model_results, scroll='third', filename=filename)

  flash('Invalid file format - please try your upload again.')
  return redirect(url_for('assess_input'))


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)
