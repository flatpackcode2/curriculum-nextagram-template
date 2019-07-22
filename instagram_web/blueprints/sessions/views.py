from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User
from werkzeug.security import check_password_hash
from flask_login import LoginManager, login_user, current_user, logout_user

sessions_blueprint = Blueprint('sessions',
                                __name__,
                                template_folder='templates/sessions')

#render login form
@sessions_blueprint.route('/login', methods=['GET'])
def new():
    return render_template('new.html')


#create a new session ie. login in to nextagram
@sessions_blueprint.route('/login', methods=['POST'])
def create():
    #collect username and password
    username = request.form['username']
    password = request.form['password']

    #check if username exists in database
    user=User.get_or_none(User.username == username)
    if user:
        if check_password_hash(user.password, password):
            # session['user_id']=user.id #manual way to log in user. Stores user id as an encrypted string in Cookies in browser.
            login_user(user)
            flash('Succesfully logged in!')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful')
            return redirect(url_for('sessions.new'))

#render homepage once logged in
@sessions_blueprint.route('/',methods=['GET'])
def index():
    return "YOU'RE LOGGED IN MUTHAFUCKA!"

@sessions_blueprint.route('/logout', methods=['GET'])
def delete():
    user = current_user
    # user.authenticated = False - do we need to create a sessions database?
    logout_user()
    return redirect(url_for('sessions.new'))
