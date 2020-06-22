from celery import shared_task
from time import sleep
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_email():
    sleep(1)
    send_mail("Ecommerce Order",
            "Your Order Is Completed!",
            "yourmailr@mail.com",
            ["receiver@mail.com"])
    return None

