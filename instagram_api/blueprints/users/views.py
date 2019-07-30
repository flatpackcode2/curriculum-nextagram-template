from flask import Flask, Blueprint, jsonify, make_response
from models.user import User


users_api_blueprint = Blueprint('users_api',
                             __name__,
                             template_folder='templates')

@users_api_blueprint.route('/', methods=['GET'])
def index():
    users = User.select()

    user_list = []
    for user in users:
        user_list.append({
           'id': user.id,
           'first_name':user.first_name,
           'last_name' : user.last_name,
           'profile_pic_url':user.profile_image_url
        })
    response= {'data':user_list}
    return make_response(jsonify(response),200)