import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from models.user import User
from flask import render_template

#Create a helper function for thank you emails after payment
def payment_email(recepient_name, donor_email, donation):
    print('payment_email triggered')
    message = Mail(
    from_email= os.getenv('CORPORATE_EMAIL'),
    to_emails= donor_email,
    subject=f'Your donation to {recepient_name} has been successful',
    html_content=render_template('/donations/email.html', donation=donation, recepient_name = recepient_name)
    )
    breakpoint()

    try:
        print('try triggered')
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)

    except Exception as e:
        print('Something has gone wrong')
        print(str(e))

#Create a helper function for password reset email
