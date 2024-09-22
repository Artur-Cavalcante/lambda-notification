import os
from datetime import datetime
from aws_lambda_powertools import Logger

from src.services.email_service import EmailService

class NotificacaoService():
    def __init__(self, logger: Logger) -> None:
        self.logger = logger
        self.email_service = EmailService(self.logger)
    
    def enviar_notificacao(self, agendamento: dict) -> bool:
        self.logger.info(f'Iniciando fluxo notificacao {agendamento}')
        to_emails = [agendamento["email_para_envio"]]
        subject = "Health&Med - Nova consulta agendada"

        if agendamento["status_agendamento"] == "Confirmado":
            if(agendamento["para_email_medico"]):
                body_html = f"""
                        <html>
                            <body>
                                <h1>Olá, Dr. {agendamento["nome_medico"]}</h1>
                                <p></p>
                                <p>Paciente: {agendamento["nome_paciente"]}</p> 
                                <p>Data e horário: {self.__format_time(agendamento["horario"])}</p> 
                            </body>
                        </html>
                        """
            else:
                body_html = f"""
                    <html>
                        <body>
                            <h1>Olá, {agendamento["nome_paciente"]}</h1>
                            <p></p>
                            <p>Você tem uma nova consulta marcada! </p>
                            <p>Médico: {agendamento["nome_medico"]}</p> 
                            <p>Data e horário: {self.__format_time(agendamento["horario"])}</p> 
                        </body>
                    </html>
                    """
        
        if agendamento["status_agendamento"] == 'Rejeitado':
            body_html = f"""
                <html>
                    <body>
                        <h1>Agendamento Rejeitado.</h1>
                        <p>Não foi possível realizar o agendamento, horário não disponível.</p>
                        <p>Horário Agendamento: {self.__format_time(agendamento["horario"])}</p> 
                        <p>CRM Médico: {agendamento["crm_medico"]}</p> 
                        <p>Paciente: {agendamento["nome_paciente"]}</p> 
                    </body>
                </html>
                """
    
        self.logger.info(f'Iniciando envio do email {agendamento}')
        self.email_service.enviar_email(to_emails, subject, body_html)
        self.logger.info(f'Finalizado envio do email {agendamento}')


    def __format_time(self, time_string):
        dt = datetime.strptime(time_string, "%Y-%m-%dT%H:%M")
        formatted_time = f'{dt.strftime("%d/%m/%Y")} às {dt.strftime("%H:%M")}'
        
        return formatted_time