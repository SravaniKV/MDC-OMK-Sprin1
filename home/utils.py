from django.conf import settings

import twilio
import twilio.rest
from twilio.rest import Client

def send_twilio_message(to_number, body):
    client = Client(
        settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    return client.messages.create(
        body=body,
        to=to_number,
        #to='+14026120202',
        from_='+15312017692'
    )
