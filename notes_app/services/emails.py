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
    def send_requested_note(email, note):
        # todo: add method to send selected note to requesting user
        pass

