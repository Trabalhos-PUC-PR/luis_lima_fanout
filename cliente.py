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

nome_chave = argv[1]

# cria uma fila caso não exista, garante que vai ter uma fila
canal.queue_declare(queue=nome_chave, auto_delete=True)

msg = ""
while msg != "fim":
    sevInt = int(input("Severidade: ((1)DEBUG|(2)INFO|(3)WARNING|(4)ERROR|(5)CRITICAL) "))
    msg = input("Mensagem: ")
    severidade = getSeveridade(sevInt)
    if(not(severidade == None)):
        canal.basic_publish(
                exchange="",
                routing_key=nome_chave,
                body=f"{time.time()}:{os.getpid()}:{severidade}:{msg}")
    else:
        print("Severidade invalida!")

conexao.close()


