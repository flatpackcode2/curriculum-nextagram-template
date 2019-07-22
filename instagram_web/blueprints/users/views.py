from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')
from flask_login import current_user, login_user, login_required


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    
    errors=[]

    if len(password) <6:
        errors.append('Password too short')
        return render_template('users/new.html', errors=errors)
    
    else:
        hashed_password = generate_password_hash(password)        
        user = User(first_name=first_name, last_name=last_name, username=username, password=hashed_password, email=email)

        if user.save():
            flash('Account successfully created')
            return redirect(url_for('home'))
        else:
            return render_template('users/new.html', errors=user.errors)


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
    user = User.get_by_id(id)
    if current_user == user: #current_user.is_authenticated?
        return render_template('users/edit.html')
    else:
        #how to show error page for unauthorized access
        return render_template('403.html'), 403


@users_blueprint.route('/<id>', methods=['POST'])
@login_required
def update(id):
    username = request.form.get('username')
    email = request.form.get('email')
    # Password needs a separate form / double-checking.
    # password = request.form.get('password')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    
    pass
    