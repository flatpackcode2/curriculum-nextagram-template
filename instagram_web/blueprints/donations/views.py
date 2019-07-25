from models.user import User
from flask import Flask, Blueprint, request, render_template, redirect, url_for, flash
from flask_login import current_user
from helpers.bt_helpers import gateway
from helpers.mail_helpers import payment_email
from models.donation import Donation
from decimal import *
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

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
    recepient_name = request.form['recepient_name']
    #need to do regex validation for entries in donation_value. r=\b[\d]{1,5}\.\d\d\b

    #if nonce exists, submit payment. 
    if nonce:
        donation = Donation(donation_value=donation_value, recepient_name = recepient_name, donor= current_user.id)
        donation.save()
        result = gateway.transaction.sale({
                    "amount": Decimal(donation_value),
                    "payment_method_nonce": nonce,
                    "options": {
                    "submit_for_settlement": True
                    }
        })
        # output = payment_email(recepient_name = recepient_name, donor_email='colinnoahpeter@gmail.com', donation=donation)
        message = Mail(
            from_email= 'welcome@nextagram.com',
            to_emails= 'colinpeter.nus@gmail.com',
            subject=f'Your donation has been successful',
            html_content= '<h1>WTFFFFFFFFFFFFF</h1>'
        )
        try:
            breakpoint()
            print('try triggered')
            sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)

        except Exception as e:
            print('Something has gone wrong')
            print(str(e))
            return render_template('/donations/failure.html')
        
        return render_template('/donations/success.html')
