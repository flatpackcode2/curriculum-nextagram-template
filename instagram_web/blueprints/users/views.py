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


#displays all users & index
@users_blueprint.route('/', methods=['GET'])
def index():
    users= User.select().where(User.username!=current_user.username)
    return render_template('users/index.html', users=users)


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
            return redirect(url_for('users.index'))
        else:
            return render_template('users/new.html', errors=user.errors)


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    user=User.get(User.username == username)
    return render_template('users/show.html', user=user)

@users_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
    user = User.get_by_id(id)
    if current_user == user: #current_user.is_authenticated?
        return render_template('users/edit.html')
    else:
        #how to show error page for unauthorized access
        return render_template('403.html'), 403


#REFACTOR THE CODE FOR update(id)
@users_blueprint.route('/<id>', methods=['POST'])
@login_required
def update(id):
    #get user by id
    user=User.get_by_id(id)

    new_username=''
    new_email=''
    new_firstname=''
    new_lastname=''
    message=[]

    #1. get username from form
    username = request.form.get('username')

    #check for changes in form
    #check if value has been deleted
    if username!='' and username!=current_user.username:
        #check if username exists
        if not User.get_or_none(User.username == username):
            new_username=username
        else:
            flash('Username is already taken')
            return redirect(url_for('users.edit', id=id))
    else:
        new_username = current_user.username
    
    #Update email
    email = request.form.get('email')
    
    if email!='' and email!=current_user.email:
        if not User.get_or_none(User.email == email):
            new_email=email
        else:
            flash('Email is already taken')
            return redirect(url_for('users.edit', id=id))

    else:
        new_email = current_user.email

    if email!='':
        #check if username exists
        if not User.get_or_none(User.email == email):
            new_email=email
    else:
        new_email=user.email
    
    #Update first_name
    firstname = request.form.get('first_name')
    if firstname!='':
        new_firstname=firstname
    else:
        new_firstname=user.first_name

    #Update last_name
    lastname = request.form.get('last_name')
    if lastname!='':
        new_lastname=lastname
    else:
        new_lastname=user.last_name

    #Username validation - to see if there is a function to do this in the model

    #Update user model
    q = User.update({'username':new_username, 'email':new_email, 'first_name':new_firstname, 'last_name':new_lastname}).where(User.id==id)  
    q.execute()
    return redirect(url_for('users.edit', id=id))