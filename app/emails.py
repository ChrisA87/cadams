from flask import render_template, current_app
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient


def send_email(to_email, subject, template, **kwargs):
    message = Mail(
        from_email='chris@cadams.app',
        to_emails=to_email,
        subject=subject,
        html_content=render_template(f'{template}.html', **kwargs))

    try:
        sg = SendGridAPIClient(current_app.config.get('SENDGRID_API_KEY'))
        sg.send(message)
    except Exception:
        pass
