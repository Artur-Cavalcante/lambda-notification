import json
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.data_classes import event_source, SQSEvent

from src.notificacao_service import NotificacaoService

logger = Logger(service="notificacao-agendamento") 
notificacao_service = NotificacaoService(logger)

@event_source(data_class=SQSEvent)
def lambda_handler(event: SQSEvent, context) -> dict:
    try:
        for record in event.records:
            logger.info(f"Event: {record.body}")
            notificacao_service.enviar_notificacao(json.loads(record.body))
        return {
            "status_code": 200,
            "body": "Sucesso"
        }
    except Exception as ex:
        logger.error(f"Erro ao processar notificação: {ex}")
        return {
            "status_code": 500,
            "body": "Erro ao processar evento"
        }

# event = {
#     "Records": [
#         {
#             "body": {
#                 "id_agendamento": 123,
#                 "id_cliente": 456,
#                 "email_cliente": "yan.kelvin@hotmail.com",
#                 # "erro": True,
#                 "itens": [ //TODO informações
#                     {
#                         "nome": "hamburguer",
#                         "quantidade": 2,
#                         "valor": 40.0
#                     },
#                     {
#                         "nome": "refrigerante",
#                         "quantidade": 2,
#                         "valor": 8.50
#                     }
#                 ]
#             }
#         }
#     ]
# }
