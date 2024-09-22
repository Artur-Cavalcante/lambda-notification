import os
from aws_lambda_powertools import Logger

from src.services.email_service import EmailService
from src.agendamento_status_enum import AgendamentoStatus

class NotificacaoService():
    def __init__(self, logger: Logger) -> None:
        self.logger = logger
        self.email_service = EmailService(self.logger)
    
    def enviar_notificacao(self, agendamento: dict) -> bool:
        to_emails = [agendamento["email_para_envio"]]
        subject = f"Agendamento {agendamento['id']}"


        if agendamento["status_agendamento"] ==  AgendamentoStatus.Confirmado:
            body_html = f"""
                    <html>
                        <body>
                            <h1>Agendamento realizado com sucesso</h1>
                            <p>Horário Agendamento: {agendamento["horario"]}</p> 
                            <p>CRM Médico: {agendamento["crm_medico"]}</p> 
                            <p>Paciente: {agendamento["nome_paciente"]}</p> 
                        </body>
                    </html>
                    """
        
        if agendamento["status_agendamento"] ==  AgendamentoStatus.Rejeitado:
            body_html = f"""
                <html>
                    <body>
                        <h1>Agendamento Rejeitado.</h1>
                        <p>Não foi possível realizar o agendamento, horário não disponível.</p>
                        <p>Horário Agendamento: {agendamento["horario"]}</p> 
                        <p>CRM Médico: {agendamento["crm_medico"]}</p> 
                        <p>Paciente: {agendamento["nome_paciente"]}</p> 
                    </body>
                </html>
                """

        self.email_service.enviar_email(to_emails, subject, body_html)
