from flask import Blueprint, render_template, flash, send_from_directory
from dlpipeline.demo.web_app.app.config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS

uploads = Blueprint('uploads', __name__, template_folder='templates')


@uploads.route('/<filename>')
def send_file(filename):
  return send_from_directory(UPLOAD_FOLDER,
                             filename)
