import os
import ssl
import time
import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart


class EmailSender:
    def __init__(self, sender, password, receiver, subject=None):
        self.email_sender = sender
        self.email_password = password
        self.email_receiver = receiver
        self.email_subject = subject
        self.email_body = open('EMail_body', 'r').read()

    def set_message(self, images=None, attachments=None, audio=None):
        """
        :param images:      list of images (given as relative paths)
        :param attachments: list of attachments (given as absolute paths)
        :param audio:       list of audio attachments (given as absolute paths)
        :return:            message containing the subject, body text and additional attachment files
        """
        message = MIMEMultipart()
        message['Subject'] = self.email_subject
        message.attach(MIMEText(self.email_body))

        # Make sure any type of file attachments (txt, images, audio etc.) are list

        if images is not None:
            images = list(images)
            for img_item in images:
                img_data = open(img_item, 'rb').read()
                # Attach the image data to MIMEMultipart
                # using MIMEImage, we add the given filename use os.basename
                message.attach(MIMEImage(img_data, name=os.path.basename(img_item)))

        if attachments is not None:
            attachments = list(attachments)
            for att_item in attachments:
                with open(att_item, 'rb') as file:
                    file = MIMEApplication(file.read(), name=os.path.basename(att_item))
                file['Content-Disposition'] = f'attachment;\
                filename="{os.path.basename(att_item)}"'
                # At last, Add the attachment to our message object
                message.attach(file)

        if audio is not None:
            audio = list(audio)
            # useful link: https://www.programcreek.com/python/example/92099/email.mime.audio.MIMEAudio
            for audio_item in audio:
                with open(audio_item, 'rb') as file:
                    audio_data = file.read()
                    c_type = 'application/octet-stream'
                    _, subtype = c_type.split("/", 1)
                item = MIMEAudio(audio_data, _subtype=subtype)
                item.add_header('Content-Disposition', "attachment; filename= %s" % os.path.basename(audio_item))
                message.attach(item)

        return message

    def send_email(self, images=None, attachments=None, audio=None,
                   scheduled_time=False, year=None, month=None, day=None, hour=None, minute=None):
        """
        Other useful libraries:
        https://pypi.org/project/hickory/ for macOS and Linux
        https://pypi.org/project/python-crontab/ for Windows

        :param images:          image files
        :param attachments:     other files
        :param audio:           audio files
        :param scheduled_time:  bool (True if the email is scheduled for a specific time, False otherwise)
        :param year:            int
        :param month:           int
        :param day:             int
        :param hour:            int
        :param minute:          int
        :return:
        """
        # add paths for images and/or attachments if necessary, example:
        # msg = self.set_message(r"C:\Users\Dell\Downloads\Garbage\Cartoon.jpg",  # image
        #                        r"C:\Users\Dell\Desktop\slack.py")  # attachment
        email = self.set_message(images, attachments, audio)
        context = ssl.create_default_context()  # layer of security
        try:
            smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context)
            smtp.ehlo()
            smtp.login(self.email_sender, self.email_password)
            if scheduled_time:
                send_time = datetime.datetime(year, month, day, hour, minute, 0)
                # print(f'send_time timestamp: {send_time.timestamp()}')
                # print(f'time.time(): {time.time()}')
                time.sleep(send_time.timestamp() - time.time())
            smtp.sendmail(self.email_sender, self.email_receiver, email.as_string())
            print('Email sent successfully.')
        except (Exception, ValueError) as e:
            print("Sent failed.\nError:", e)


def send_out_email(sender, password, receiver, subject='',                                          # credentials
                   images=None, attachments=None, audio=None,                                       # attachment files
                   scheduled_time=False, year=None, month=None, day=None, hour=None, minute=None):  # send time
    em = EmailSender(sender, password, receiver, subject)
    em.send_email(images, attachments, audio, scheduled_time, year, month, day, hour, minute)


if __name__ == "__main__":
    send_out_email(
        sender='andreea.munteanu05@gmail.com',
        password='duyuqvssdlmmqakj',
        receiver=['andreea.munteanu05@gmail.com'],
        subject='Subject is subject',
        attachments=[r"C:\Users\AEMunteanu\Desktop\netflix_data.txt"],
        audio=[r"C:\Users\AEMunteanu\Downloads\LP_-_Lost_On_You_Official_Music_Video[ConverteZilla.com].mp3"],
        scheduled_time=True, year=2022, month=9, day=14, hour=11, minute=42
    )
