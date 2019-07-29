from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User
from werkzeug.security import check_password_hash
from flask_login import LoginManager, login_user, current_user, logout_user

sessions_blueprint = Blueprint('sessions',
                                __name__,
                                template_folder='templates/sessions')
from helpers.google_oauth import oauth

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
            flash('Successfully logged in!')
            return redirect(url_for('users.index'))
        else:
            flash('Login unsuccessful. Please check username & password')
            return redirect(url_for('sessions.new'))
    else:
        flash('User does not exist')
        return redirect(url_for('sessions.new'))

@sessions_blueprint.route('/logout', methods=['GET'])
def delete():
    user = current_user
    # user.authenticated = False - do we need to create a sessions database?
    logout_user()
    return redirect(url_for('sessions.new'))

@sessions_blueprint.route('/new/google', methods=['GET'])
#serve google login?
def google_login():
    redirect_uri = url_for('sessions.authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@sessions_blueprint.route('/authorize/google', methods=['GET'])
def authorize():
    token = oauth.google.authorize_access_token()
    response = oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo')
    email = response.json()['email']

    user = User.get_or_none(User.email == email)

    if not user:
            flash('User does not exist. Please sign-up here')
            return render_template('users/new.html')
    
    login_user(user)
    flash('Welcome back!')
    return redirect(url_for('users.index'))
