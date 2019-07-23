from models.image import User
from flask import Flask, Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required
from werkzeug.utils import secure_filename
from helpers import upload_file_to_S3
from config import *

images_blueprint = Blueprint('images', __name__, template_folder='templates')

#Upload a profile image
@images_blueprint.route('/<id>/new', methods=['GET', 'POST'])
@login_required
def create(id):
    if request.method=="POST":
        user = User.get_by_id(id)
        if not 'image_file' in request.files:
            flash('No file provided')
            return redirect(url_for('images.create', id=id))
        
        image_file = request.files['image_file']

        if image_file.filename != '':
            image_file.filename= secure_filename(image_file.filename)
            q=User.update({User.profile_image:image_file.filename}).where(User.id==id)
            q.execute()
            output = upload_file_to_S3(image_file)

    return render_template('images/new .html')