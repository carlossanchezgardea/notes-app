from dotenv import load_dotenv
import requests
import os

load_dotenv()
sendgrid_key = os.environ.get("sendgrid_api")


class SendGridMailer:

    def __init__(self):
        self.api_key = sendgrid_key
        self.url = "https://api.sendgrid.com/v3/mail/send"
        self.headers = {
            'Authorization': f'Bearer {sendgrid_key}',
            'Content-Type': 'application/json'
        }

    def send_email(self, to_email, template_id, dynamic_template_data):
        payload = {
            "from": {"email": 'hola@ailofi.co'},
            "personalizations": [
                {
                    "to": [{"email": to_email}],
                    "dynamic_template_data": dynamic_template_data
                }
            ],
            "template_id": template_id
        }

        response = requests.post(self.url, headers=self.headers, json=payload)

        if response.status_code == 202:
            print("Email sent successfully.")
        else:
            print(f"Failed to send email. Status code: {response.status_code}, Reason: {response.text}")


# send = SendGridMailer()
# send.send_email('carlos@nelo.co', 'd-599f54359f394e21bac573a44d1aaaa0', {'first_name': 'popo'})
