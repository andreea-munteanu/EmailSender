import os
import ssl
import smtplib
# from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart


class EmailSender:
    def __init__(self, sender, password, receiver, subject=None, body_text=open('EMail_body', 'r').read()):
        self.email_sender = sender
        self.email_password = password
        self.email_receiver = receiver
        self.email_subject = subject
        self.email_body = body_text

    # def set_up_email(self):
    #     """ Doesn't allow for file attachments, use MIME instead. """
    #     email = EmailMessage()
    #     email['From'] = self.email_sender
    #     email['To'] = self.email_receiver
    #     email['Subject'] = self.email_subject
    #     email.set_content(self.email_body)
    #     return email

    def set_message(self, images=None, attachments=None):
        """
        :param images: list of images (given as relative paths)
        :param attachments: list of attachments (given as relative paths)
        :return:
        """
        message = MIMEMultipart()
        message['Subject'] = self.email_subject
        message.attach(MIMEText(self.email_body))

        # Make sure image and other file attachments are lists to allow for multiple items to be attached to email:

        if images is not None:
            if type(images) is not list:
                images = [images]
            for img_item in images:
                img_data = open(img_item, 'rb').read()
                # Attach the image data to MIMEMultipart
                # using MIMEImage, we add the given filename use os.basename
                message.attach(MIMEImage(img_data, name=os.path.basename(img_item)))

        if attachments is not None:
            if type(attachments) is not list:
                attachments = [attachments]
            for att_item in attachments:
                with open(att_item, 'rb') as f:
                    file = MIMEApplication(f.read(), name=os.path.basename(att_item))
                file['Content-Disposition'] = f'attachment;\
                filename="{os.path.basename(att_item)}"'
                # At last, Add the attachment to our message object
                message.attach(file)

        return message

    def send_email(self, images=None, attachments=None):
        # add paths for images and/or attachments if necessary, example:
        # msg = self.set_message(r"C:\Users\Dell\Downloads\Garbage\Cartoon.jpg",  # image
        #                        r"C:\Users\Dell\Desktop\slack.py")  # attachment
        email = self.set_message(images, attachments)
        context = ssl.create_default_context()  # layer of security
        try:
            smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context)
            smtp.ehlo()
            smtp.login(self.email_sender, self.email_password)
            smtp.sendmail(self.email_sender, self.email_receiver, email.as_string())
            smtp.quit()
            print('Email sent successfully.')
        except (Exception, ValueError) as e:
            print("Sent failed.\n", e)


if __name__ == "__main__":
    em = EmailSender(sender='andreea.munteanu05@gmail.com',
                     password='insert-your-pass-here',
                     receiver=['andreea.munteanu05@gmail.com'],
                     subject='Test run')
    em.send_email(attachments=r"C:\Users\AEMunteanu\Desktop\netflix_data.txt")
