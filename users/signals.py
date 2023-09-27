# your_app_name/signals.py
import random
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from django.conf import settings

User =get_user_model()


@receiver(pre_save, sender=User)
def send_otp_email(sender, instance, **kwargs):
    print("singanl")
    if not instance.otp:
        # Generate a 6-digit OTP
        otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        settings.OTP_SETTINGS['otp'] = otp
        instance.otp = otp

        # Send OTP via email
        subject = 'Your OTP for Account Verification'
        message = f'Your OTP is: {otp}'
        from_email = 'anaghaponnore2000@gmail.com'  # Replace with your email
        recipient_list = ['anaghaponnore2000@gmail.com']

        send_mail(subject, message, from_email, recipient_list)


        # # # Store OTP in the session
        # session_key = f'otp_{instance.pk}'  # Use the user's primary key as part of the session key

        # request = getattr(instance, '_request', None)  # Get the request object if it's set
        # if request:
        #     session = request.session  # Use the request's session
        # else:
        #     session = SessionStore()  # Create a new session if no request is available

        # session[session_key] = otp
        # session.save()
        # print(session[session_key])
        instance.save()
        print("mail")
    