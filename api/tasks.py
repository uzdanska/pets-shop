from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

@shared_task
def send_payment_reminder_email(user_email):
    subject = 'Przypomnienie o płatności'
    message = 'Przypominamy o zbliżającym się terminie płatności. Prosimy uregulować płatność przed jutrzejszym dniem.'
    from_email = 'twoj@example.com'  
    recipient_list = [user_email]
    
    send_mail(subject, message, from_email, recipient_list)