# importando o modulo socket
import socket

import datetime

from nsip import *

# definindo a porta do servidor
PORTANUMERO = 2102

# criando um socket Internet (INET IPv4) sobre UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# liga o socket ao enderecamento do servidor
s.bind(("", PORTANUMERO))

print("Servidor escutando conexoes UDP na porta: %d\n" % PORTANUMERO)

while True:
    # aguardando requisicao 
    buffer, clientaddress = s.recvfrom(500)
    print("Recebida uma mensagem do endereço %s" % clientaddress[0])

    # formatando a hora atual
    hora_atual = datetime.datetime.now()
    hora_atual_bytes = hora_atual.strftime("%c").encode("ISO-8859-1")

    print("Enviando a hora atual: %s\n" % hora_atual)

    # enviando a hora para o cliente
    s.sendto(hora_atual_bytes, clientaddress)