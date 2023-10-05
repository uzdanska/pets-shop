from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .models import Order
from datetime import timedelta
from django.utils import timezone

@shared_task
def send_payment_reminder_email():
    tomorrow = timezone.now().date() + timedelta(days=1)
    order_to_remind = Order.objects.filter(paymentDue=tomorrow)
    print(order_to_remind)
    for order in order_to_remind:
        subject = 'Przypomnienie o płatności'
        message = 'Przypominamy o zbliżającym się terminie płatności. Prosimy uregulować płatność przed jutrzejszym dniem.'
        from_email = 'twoj@example.com'  
        recipient_list = [order.customer.user.email]
    
        send_mail(subject, message, from_email, recipient_list)

