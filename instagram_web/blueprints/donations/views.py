from models.user import User
from flask import Flask, Blueprint, request, render_template, redirect, url_for, flash
from flask_login import current_user
from helpers.bt_helpers import gateway
from models.donation import Donation
from decimal import *

getcontext().prec = 2

donations_blueprint = Blueprint('donations', __name__, template_folder='templates')

@donations_blueprint.route('/new/<username>', methods=["GET"])
def new(username):
    client_token = gateway.client_token.generate()
    return render_template('donations/new.html', client_token=client_token, username=username)

@donations_blueprint.route('/checkout', methods=["POST"])
def payment():
    nonce= request.form["payment_method_nonce"]
    donation_value = request.form['donation_value']
    recepient =request.form['recepient']
    #need to do regex validation for entries in donation_value. r=\b[\d]{1,5}\.\d\d\b

    #if nonce exists, submit payment. 
    if nonce:
        donation = Donation(donation_value=donation_value, recepient = recepient, donor= current_user.id)
        donation.save()
        result = gateway.transaction.sale({
                    "amount": Decimal(donation_value),
                    "payment_method_nonce": nonce,
                    "options": {
                    "submit_for_settlement": True
                    }
        })
        return redirect('/donations/success.html')
    
    return render_template('/donations/failure.html')