#!/usr/bin/python3

from sys import argv
from pika import BlockingConnection

verbose = True

def callback(channel, method, properties, body):
    global verbose
    msg = body.decode()
    # ts:sev:pid:comment
    # verbose:on/off
    splits = msg.split(':')
    if(len(splits) == 4):
        if(verbose):
            print(splits[3])
        return

    elif(len(splits) == 2):
        if (not(splits[0]=='verbose')):
            print('sintaxe invalida!')
            return
        if(splits[1] == 'on'):
            verbose = True
        elif(splits[1] == 'off'):
            verbose = False
        else:
            print('sintaxe do verbose invalida!')
            return
    else:
            print('sintaxe do logger invalida!')
            return

# broker
conexao = BlockingConnection()

# channel
canal = conexao.channel()

nome_chave = argv[1]

# cria uma fila caso não exista, garante que vai ter uma fila
canal.queue_declare(queue=nome_chave, auto_delete=True)

# publica o canal, usa o exchange padrão, routing key
canal.basic_consume(
        queue=nome_chave,
        on_message_callback=callback,
        auto_ack=True)

try:
    print("Aguardando mensagens")
    canal.start_consuming()
except KeyboardInterrupt:
    canal.stop_consuming()

conexao.close()


