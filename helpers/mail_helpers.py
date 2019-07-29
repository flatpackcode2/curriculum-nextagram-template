import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from models.user import User
from flask import render_template, request, url_for

#Create a helper function for thank you emails after payment
def payment_email(recepient_name, donor_email, donation):
    print('payment_email triggered')
    message = Mail(
    from_email= os.getenv('CORPORATE_EMAIL'),
    to_emails= 'colinnoahpeter@gmail.com',
    subject=f'Your donation to {recepient_name} has been successful',
    html_content=render_template('/donations/email.html', donation=donation, recepient_name = recepient_name)
    )

    try:
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return True

    except Exception as e:
        print(str(e))
        return False


#email to request idol to approve fan
def approval_email(fan, idol):
    message = Mail(
    from_email = os.getenv('CORPORATE_EMAIL'),
    to_emails='colinnoahpeter@gmail.com',
    subject=f"{fan.username} has requested to follow you,{idol.username}",
    html_content=f"<p>Approve them by clicking <a href='http://localhost:5000{url_for('followers.edit_approval', id = idol.id)}/edit'>here</a></p>"
    )
    try:
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return True

    except Exception as e:
        print(str(e))
        return False

#Create a helper function for password reset email
