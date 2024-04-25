#!/usr/bin/python3

import time
import os
from sys import argv
from pika import BlockingConnection

def getSeveridade(sev):
    msg = None
    if(sev==1):
        msg = "DEBUG"
    elif(sev==2):
        msg = "INFO"
    elif(sev==3):
        msg = "WARNING"
    elif(sev==4):
        msg = "ERROR"
    elif(sev==5):
        msg = "CRITICAL"
    return msg

# broker
conexao = BlockingConnection()

# channel
canal = conexao.channel()

# recebendo o nome do exchange
nome_exchange = argv[1]

# declarando uma exchange caso nao exista, com o nome acima, do tipo fanout
canal.exchange_declare(exchange=nome_exchange, exchange_type='fanout')

msg = ""
while msg != "fim":
    severidade = 0
    isMsg = False
    msg = input("Mensagem(verbose:[on/off]): ")

    if(msg.split(':')[0] != 'verbose'):
        isMsg = True
        sevInt = int(input("Severidade: ((1)DEBUG|(2)INFO|(3)WARNING|(4)ERROR|(5)CRITICAL) "))
        severidade = getSeveridade(sevInt)

    if(severidade != None):
        if(isMsg):
            msgBody = f"{time.time()}:{os.getpid()}:{severidade}:{msg}"
        else:
            msgBody = msg

        canal.basic_publish(
                exchange=nome_exchange,
                routing_key="",
                body=msgBody)

    else:
        print("Severidade invalida!")

conexao.close()


