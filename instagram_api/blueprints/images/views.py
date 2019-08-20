from flask import Flask, Blueprint, jsonify, make_response, request
from flask_login import current_user
from flask_jwt_extended import get_jwt_identity, jwt_required
from models.image import Image
from models.user import User
from werkzeug.utils import secure_filename
from helpers.im_helpers import upload_file_to_S3


images_api_blueprint = Blueprint('images_api',
                             __name__,
                             template_folder='templates')

# POST request to upload profile picture
@images_api_blueprint.route('/', methods=['POST'])
@jwt_required
def create():
   #get jwt identity and post image
   user_id = get_jwt_identity() #when creating access token, user.id is used as identity in JWT Token. this is encoded into base64. get_jwt_identity decodes it.
   #where do i get authorization header from? is this from JWT from browser when front end makes api call?
   user = User.get_by_id(user_id)
   image_file = request.files.get('image_file', None)

   if image_file == None:
      response = {'Message': 'No file provided'}
      return make_response(jsonify(response),400)
   
   image_file.filename = secure_filename(image_file.filename)
   q=User.update({User.profile_image:image_file.filename}).where(User.id==user_id)
   q.execute()
   output = upload_file_to_S3(image_file)
   response = {'message': 'profile image upload successful', 'url': output}
   return make_response(jsonify(response), 200)