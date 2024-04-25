#!/usr/bin/python3

from sys import argv
from pika import BlockingConnection

verbose = True

def validaSeveridade(sev):
    msg = ""
    if(sev== "DEBUG"):
        pass
    elif(sev=="INFO"):
        pass
    elif(sev== "WARNING"):
        pass
    elif(sev== "ERROR"):
        pass
    elif(sev== "CRITICAL"):
        pass
    else:
        msg = None
    return msg

def callback(channel, method, properties, body):
    global verbose
    msg = body.decode()
    splits = msg.split(':')
    # ts:sev:pid:comment
    if(len(splits) == 4):
        if(verbose and (validaSeveridade(splits[2]) != None)):
            print(f'{splits[0]}|pid:{splits[1]}|{splits[2]}: {splits[3]}')
            return
        else:
            print('severidade invalida!')
            return

    # verbose:on/off
    elif(len(splits) == 2):
        if (not(splits[0]=='verbose')):
            print('body invalido!')
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

nome_exchange = argv[1]

canal.exchange_declare(exchange=nome_exchange, exchange_type='fanout')

result = canal.queue_declare(queue='', exclusive=True)
nome_queue = result.method.queue
canal.queue_bind(exchange=nome_exchange, queue=nome_queue)

print(f'ouvindo na fila {nome_queue}...')
# publica o canal, usa o exchange padrão, routing key
canal.basic_consume(
        queue=nome_queue,
        on_message_callback=callback,
        auto_ack=True)

try:
    print("Aguardando mensagens")
    canal.start_consuming()
except KeyboardInterrupt:
    canal.stop_consuming()

conexao.close()


