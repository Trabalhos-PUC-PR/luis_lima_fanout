#!/usr/bin/python3

from sys import argv
from pika import BlockingConnection

# broker
conexao = BlockingConnection()

# channel
canal = conexao.channel()

nome_chave = argv[1]

# cria uma fila caso não exista, garante que vai ter uma fila
canal.queue_declare(queue=nome_chave, auto_delete=True)

msg = ""
while msg != "fim":
    msg = input("Mensagem: ")
    canal.basic_publish(
            exchange="",
            routing_key=nome_chave,
            body=f"{msg}")

conexao.close()


