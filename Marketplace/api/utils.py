
from twilio.rest import Client
import random
from django.conf import settings

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_via_sms(phone_number, otp):
    client = Client("AC59f803764a378914df0f4f260845834b", "73e54338d8c7e1cbd27f4cded27c0026")
    message = client.messages.create(
        body=f'Your OTP is: {otp}',
        from_="+12513024483",
        to=phone_number
    )
    return message.sid
