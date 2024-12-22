from django.conf import settings
from django.core.mail import send_mail

def send_forgot_mail(request, user_obj, token):
    website_url = request.build_absolute_uri('/')[:-1]
    subject = f'Password Reset Request'
    message = f'Hi {user_obj.get_full_name()},\nClick on the link to reset your password.\n{website_url}/account/reset-password/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user_obj.get_email()]

    try:
        send_mail(subject, message, email_from, recipient_list)
        return True
    except Exception as e:
        return False