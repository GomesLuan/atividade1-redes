import socket
from nsip import *

# definindo a porta do servidor
PORTANUMERO = 2102

# criando um socket Internet (INET IPv4) sobre UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# liga o socket ao enderecamento do servidor
s.bind(("", PORTANUMERO))

print("Servidor UDP escutando na porta: %d\n" % PORTANUMERO)

def process_request(packet):
    if packet.type == NSIP_REQ:
        packet.type = NSIP_REP
        if packet.query == SYS_PROCNUM:
            packet.result = str(len(psutil.pids()))
        elif packet.query == SYS_BOOTIME:
            packet.result = str(psutil.boot_time())
        elif packet.query == CPU_COUNT:
            packet.result = str(psutil.cpu_count())
        elif packet.query == CPU_PERCT:
            packet.result = str(psutil.cpu_percent(interval=1))
        elif packet.query == CPU_STATS:
            stats = psutil.cpu_stats()
            packet.result = f"{stats.ctx_switches},{stats.interrupts}"
        elif packet.query == MEM_TOTAL:
            packet.result = str(psutil.virtual_memory().total)
        elif packet.query == MEM_FREE:
            packet.result = str(psutil.virtual_memory().available)
        elif packet.query == MEM_PERCT:
            packet.result = str(psutil.virtual_memory().percent)
        elif packet.query == DISK_PARTS:
            partitions = psutil.disk_partitions()
            packet.result = ",".join(part.device for part in partitions)
        elif packet.query == DISK_USAGE:
            usage = [str(psutil.disk_usage(part.device).percent) for part in psutil.disk_partitions()]
            packet.result = ",".join(usage)
        elif packet.query == NET_IFACES:
            packet.result = ",".join(psutil.net_if_addrs().keys())
        elif packet.query == NET_IPS:
            ips = [addr.address for iface in psutil.net_if_addrs().values() for addr in iface if addr.family == socket.AF_INET]
            packet.result = ",".join(ips)
        elif packet.query == NET_MACS:
            macs = [addr.address for iface in psutil.net_if_addrs().values() for addr in iface if addr.family == psutil.AF_LINK]
            packet.result = ",".join(macs)
        elif packet.query == NET_TXBYTES:
            packet.result = str(psutil.net_io_counters().bytes_sent)
        elif packet.query == NET_RXBYTES:
            packet.result = str(psutil.net_io_counters().bytes_recv)
        elif packet.query == NET_TXPACKS:
            packet.result = str(psutil.net_io_counters().packets_sent)
        elif packet.query == NET_RXPACKS:
            packet.result = str(psutil.net_io_counters().packets_recv)
        elif packet.query == NET_TCPCONS:
            packet.result = str(len(psutil.net_connections(kind='tcp')))
        elif packet.query == NET_TCPLIST:
            tcp_ports = [str(conn.laddr.port) for conn in psutil.net_connections(kind='tcp') if conn.status == psutil.CONN_LISTEN]
            packet.result = ",".join(tcp_ports)
        elif packet.query == NET_UDPCONS:
            packet.result = str(len(psutil.net_connections(kind='udp')))
        elif packet.query == NET_UDPLIST:
            udp_ports = [str(conn.laddr.port) for conn in psutil.net_connections(kind='udp')]
            packet.result = ",".join(udp_ports)
        else:
            packet.type = NSIP_ERR
            packet.result = "Consulta inválida"
    else:
        packet.type = NSIP_ERR
        packet.result = "Tipo de pacote inválido"

while True:
    # Recebe o pacote de requisição do cliente
    buffer, client_address = s.recvfrom(500)
    packet = NSIPPacket()
    packet.from_packet(buffer)
    print("Requisição recebida do cliente")
    packet.print()

    # Verificação através do checksum
    original_checksum = packet.checksum
    recalculated_checksum = checksum(packet.to_packet())
    if recalculated_checksum != original_checksum:
        packet.type = NSIP_ERR
        packet.result = "Checksum inválido"
    else: 
        result = process_request(packet)

    # Calcula e define o checksum para o pacote de resposta
    packet.checksum = checksum(packet.to_packet())

    # Envia o pacote de resposta de volta ao cliente
    s.sendto(packet.to_packet(), client_address)
    print("Resposta enviada ao cliente.")
    packet.print()