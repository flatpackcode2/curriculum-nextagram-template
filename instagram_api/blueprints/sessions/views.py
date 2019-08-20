from models.user import User
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask import Blueprint, make_response, jsonify, request
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import check_password_hash

sessions_api_blueprint = Blueprint('sessions_api', __name__, template_folder='templates')

@sessions_api_blueprint.route('/login', methods=['POST'])
def new():
    #need to check if object submitted is in json format. Use is_json
    # username = request.json.get('username', None) # if request is json
    # username = 'albert'
    # password = request.json.get('password', None) # if request is json
    # password = 'albert'
    
    username = request.form.get('username', None)
    password = request.form.get('password', None)

    user = User.get_or_none(User.username == username)
    
    if not user:
        response = {
            'message':"No such user exists"
        }

        return make_response(jsonify(response), 401)
    
    if not check_password_hash(user.password, password):
        response ={
            'message': 'Invalid password'
        }

        return make_response(jsonify(response), 401)

    access_token = create_access_token(identity=user.id)

    #access_token is the JWT
    response = {
        'message':'Successfully logged in',
        'auth_token': access_token
    }

    return make_response(jsonify(response), 200)