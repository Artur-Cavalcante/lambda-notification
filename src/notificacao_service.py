import os
from aws_lambda_powertools import Logger

from src.services.email_service import EmailService

class NotificacaoService():
    def __init__(self, logger: Logger) -> None:
        self.logger = logger
        self.email_service = EmailService(self.logger)
    
    def enviar_notificacao(self, agendamento: dict) -> bool:
        to_emails = [agendamento["email_cliente"]]
        subject = f"Agendamento {agendamento['id_agendamento']}"
        
        if "erro" in agendamento and agendamento["erro"]:
            body_html = f"""
                <html>
                    <body>
                        <h1>Erro ao realizar agendamento.</h1>
                        <p>Por favor tente novamente.</p>
                    </body>
                </html>
                """
        else:
            body_html = f"""
                    <html>
                        <body>
                            <h1>Agendamento realizado com sucesso</h1>
                            <p>Preparando pedido:</p> //TODO colocar horario 
                            <p>Total pedido: R$ {pedido['total_pedido']}</p>
                        </body>
                    </html>
                    """

        self.email_service.enviar_email(to_emails, subject, body_html)
