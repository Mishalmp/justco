from django.conf import settings
from twilio.rest import Client


def display_cred():
    print(settings.TWILIO_ACCOUNT_SID,'\n',settings.TWILIO_AUTH_TOKEN)

def send_otp_on_phone(phone_number,otp):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        from_='+19046858452',
        body=f'Hi, Welcome to Just Watches your OTP is {otp}',
        to=phone_number
        )