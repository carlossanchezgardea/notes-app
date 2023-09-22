from notes_app.clients.sendgrid_client import SendGridMailer


class EmailSender:

    @staticmethod
    def send_welcome_email(email, first_name):
        send = SendGridMailer()
        send.send_email(
            to_email=email,
            template_id='d-599f54359f394e21bac573a44d1aaaa0',
            dynamic_template_data={
                "first_name": first_name,
            }
        )

    @staticmethod
    def send_requested_note(email, title, description, body):
        send_note = SendGridMailer()
        send_note.send_email(
            to_email=email,
            template_id='d-bc5ec32784b542b3b61cc8830cee0c78',
            dynamic_template_data={
                "title": title,
                "description": description,
                "body": body
            }
        )


# send1 = EmailSender()
# send1.send_requested_note('carlos@nelo.co','title', 'description', 'body')
