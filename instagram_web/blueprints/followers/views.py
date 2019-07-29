from models.relationship import Relationship
from models.user import User
import peewee as pw
from flask import Flask, Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required

from helpers.mail_helpers import approval_email

followers_blueprint = Blueprint('followers', __name__, template_folder='templates')


#if a user types in followers/new, for some reason it gets sent to the approval page (not sure if idol's or fans)
@followers_blueprint.route('/new', methods=['GET'])
@login_required
def new():
    flash("Please visit an idol's page to follow them")
    return redirect(url_for('users.index'))

#Things to check for:
#1. What if a user tries to follow themself? Right now the user can only see other profiles in the home page.
#2. This logic will need to be implemented in the search bar and accounted for in the database. fan!=idol

@followers_blueprint.route('/', methods=['POST'])
@login_required
def create():
    fan_id = current_user.id
    idol_id= request.form.get('idol_id')
    idol = User.get_by_id(idol_id)

    #Check if fan has previously requested to follow this idol.
    follower=Relationship.get_or_none(Relationship.idol==idol_id, Relationship.fan==fan_id)

    #if they have, flash a message letting them know they have submitteed a request and redirect them to user proifle. Otherwise create a database entry.
    if follower:
        flash(f" You've already submitted a follow request to {idol.username} ")
        return redirect(url_for('users.show', username=idol.username))
    else:
        follower = Relationship(fan = fan_id, idol=idol_id)

    if follower.save():
        flash(f"You have submitted a request to follow {idol.username}")
        status = approval_email(fan=current_user, idol = idol)
        print (f'Email request sent:{status}')
        return redirect(url_for('users.show', username=idol.username))

    else:
        flash(f"Something went wrong")

@followers_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit_approval(id):
    # breakpoint()
    if current_user.id==int(id):
        print('current_user is the same')
        return render_template('followers/approve.html')
    else:
        print('else is being triggered')
        return redirect('500.html')#doesn't work. See another way.

@followers_blueprint.route('/<id>/', methods=['POST'])
@login_required
def update_approval(id):
    relationship_id = request.form['relationship_id']
    approval_status = request.form['approval_status']
    print('*******')
    print(approval_status)
    entry= Relationship.get_by_id(relationship_id)
    if approval_status=="Approve":
        print('executing update')
        q=Relationship.update(approved=True).where(Relationship.id == relationship_id)
        q.execute()
    elif approval_status=="Reject":
        print('executing delete')
        entry.delete_instance()
    return redirect(url_for('followers.edit_approval', id=id))

# #collects response on approval page of idol and subsequently adds into relationship table if approval is successful
# @followers_blueprint.route('/<id>', methods=['POST'])
# def update_approval(id):
#     status=request.
# Click approve - register with database. Else, not.
