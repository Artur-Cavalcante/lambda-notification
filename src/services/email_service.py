import os
import smtplib
from typing import List
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

from aws_lambda_powertools import Logger

class EmailService:
    def __init__(self, logger: Logger):
        self.smtp_port = 587
        self.smtp_server = "smtp.gmail.com"
        self.username = os.environ["username"]
        self.password = os.environ["password"]
        self.logger = logger

    def enviar_email(self, to_emails: List[str], subject: str, body: str, body_html: str = None, attachments: List[str] = None):
        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = ', '.join(to_emails)
        msg['Subject'] = subject

        if 'html' in body:
            msg.attach(MIMEText(body, 'html'))
        else:
            msg.attach(MIMEText(body, 'plain'))

        if attachments:
            for file_path in attachments:
                part = MIMEBase('application', 'octet-stream')
                with open(file_path, 'rb') as file:
                    part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={file_path.split("/")[-1]}')
                msg.attach(part)

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
                self.logger.info('E-mail enviado com sucesso!')
        except Exception as e:
            self.logger.error(f'Erro ao enviar e-mail: {e}')
