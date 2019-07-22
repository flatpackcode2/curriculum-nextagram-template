from models.image import User
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required
from werkzeug.utils import secure_filename

images_blueprint = Blueprint('images', __name__, template_folder='templates')

#Upload a profile image
@images_blueprint.route('/<id>/new', methods=['GET', 'POST'])
@login_required
def create(id):
    if request.method=="POST":
        user = User.get_user_by_id(id)
        uploaded_image = request.file['uploaded_image']
        
        print(uploaded_image)
        
    return render_template('images/new.html')