import socket
from nsip import *

# definindo a porta do servidor
PORTANUMERO = 2102

# criando um socket Internet (INET IPv4) sobre UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# liga o socket ao enderecamento do servidor
s.bind(("", PORTANUMERO))

print("Servidor escutando conexoes UDP na porta: %d\n" % PORTANUMERO)

while True:
    # Recebe o pacote de requisição do cliente
    buffer, client_address = s.recvfrom(500)
    req_packet = NSIPPacket()
    req_packet.from_packet(buffer)
    print("Requisição recebida do cliente")
    req_packet.print()

    # Cria a resposta baseado na consulta recebida
    if req_packet.query == SYS_PROCNUM:
        result = str(len(psutil.pids()))
    else:
        result = "Consulta não suportada"

    # Prepara o pacote de resposta
    rep_packet = NSIPPacket(
        id=req_packet.id,
        type=NSIP_REP,
        query=req_packet.query,
        result=result
    )
    rep_packet.checksum = checksum(rep_packet.to_packet())

    # Envia o pacote de resposta de volta ao cliente
    s.sendto(rep_packet.to_packet(), client_address)
    print("Resposta enviada ao cliente.")
    rep_packet.print()