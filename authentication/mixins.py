
import random
from django.conf import settings
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse

client = Client(settings.ACCOUNT_SID, settings.ACCOUNT_TOKEN)
PHONE_NUMBER = "+12314506546"

class MessageHandler:
    phone = None
    otp = None
    
    def __init__(self, phone, otp):
        self.phone = phone
        self.otp = otp
    
    def verified_number_before_sending_otp(self):
        verification = client.verify.v2.services("VAaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa").verifications.create(to=f"{self.phone}", channel="sms")
        return verification
    
    def send_otp_to_phone(self):
        message = client.messages.create(
            body=f"Your OTP for logging in to Taurus Leo account is {self.otp}. Do not share with anyone.\n-Taurus Leo",
            from_=PHONE_NUMBER,
            to=f"{self.phone}",
        )
        return message
    
    def send_otp_to_whatsapp(self):
        message = client.messages.create(
            body=f"{self.otp} is your verification code. For your security, do not share this code.",
            from_=f'whatsapp:+14155238886',
            media_url= ["https://ik.imagekit.io/harmonystudio/taurus-logo-square.png"],
            to=f'whatsapp:{self.phone}'
        )
    
    def voice_response(self):
        resp = VoiceResponse()
        resp.say(f"Your OTP for logging in to Taurus Leo account is {self.otp}.", voice='Polly.Amy')
        return str(resp)
    
    def receive_call(self):
        call = client.calls.create(
            twiml=self.voice_response(),
            to=f"{self.phone}",
            from_="+12314506546",
        )
        return call