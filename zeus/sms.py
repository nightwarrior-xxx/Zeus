from twilio.rest import Client
from zeus import settings
import os
client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)
try:
    smsMessage = client.messages \
            .create(
                body="Hello World"
                from_ = os.environ.get('TWILIO_PHONE_NUMBER'),
                to='+917982916122'
            )
    print(smsMessage.sid)
    print('SMS send')

except:
    print('SMS send failed')
