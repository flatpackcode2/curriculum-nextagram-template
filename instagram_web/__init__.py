from app import app
from flask import render_template
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from instagram_web.blueprints.images.views import images_blueprint
from instagram_web.blueprints.donations.views   import donations_blueprint
from instagram_web.blueprints.followers.views   import followers_blueprint

from flask_assets import Environment, Bundle
from .util.assets import bundles
import os
from helpers.google_oauth import oauth
import config

assets = Environment(app)
assets.register(bundles)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
app.register_blueprint(images_blueprint, url_prefix="/images")
app.register_blueprint(donations_blueprint, url_prefix="/donations")
app.register_blueprint(followers_blueprint, url_prefix="/followers")

oauth.init_app(app)

@app.route("/")
def home():
    return render_template('home.html')

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.errorhandler(403)
def unauthorized_access(e):
    # note that we set the 404 status explicitly
    return render_template('403.html'), 403