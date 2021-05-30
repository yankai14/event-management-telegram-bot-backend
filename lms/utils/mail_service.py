from django.core.mail import send_mail
from lms.utils.mail_templates import facilitator_application_mail
from lms.models.user_models import User


class MailService:

    def __init__(self, sender, receiver):
        self.sender = sender
        self.receiver = receiver # Type of either a str or a list
    
    def send_facilitator_application_mail(self, user, enrollmentData):
        subject = f"{user.first_name} {user.last_name} application for facilitator for {enrollmentData.get('eventInstanceCode')}"
        body = facilitator_application_mail
        plain_message = "Please go to your admin page to take a look at the pending requests"

        send_mail(
            subject,
            plain_message,
            self.sender,
            self.receiver,
            html_message=body,
            fail_silently=False,
        )

