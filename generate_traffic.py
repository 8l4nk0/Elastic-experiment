import os
import time
from scapy.all import *

# -i indica l'intervallo tra l'invio di un pkg e l'altro
# in questo caso abbiamo impostato 2000microsec = 1 sec
def generate_hping3_traffic(target_ip):
    print(f"Generating hping3 traffic to {target_ip}")
    os.system(f"hping3 -S -p 80 -i u2000 -c 1000 {target_ip}")

# -c indica che invia 100 pkg
def generate_nping_traffic(target_ip):
    print(f"Generating nping traffic to {target_ip}")
    os.system(f"nping --tcp -p 80 --flags syn -c 100 {target_ip}")

# -f indica flood e se non viene impostata la velocita' al
# quale inviarli, li invia a 100 pkg/s
def generate_ping_flood(target_ip):
    print(f"Generating ping flood to {target_ip}")
    os.system(f"ping -f -c 100 {target_ip}")

# 1-65535 indica di fare lo scan su tutte le porte,
# -T4 indica con quale velocita'
def generate_nmap_scan(target_ip):
    print(f"Generating nmap scan to {target_ip}")
    os.system(f"nmap -p 1-65535 -T4 {target_ip}")

# la flag S sta per SYN pkg
def generate_scapy_traffic(target_ip):
    print(f"Generating scapy TCP SYN traffic to {target_ip}")
    for i in range(100):
        send(IP(dst=target_ip)/TCP(dport=80, flags="S"))
        time.sleep(0.01)

if __name__ == "__main__":
    target_ip = "localhost"  # Sostituire con l'indirizzo IP del target

    # Genera traffico con hping3
    generate_hping3_traffic(target_ip)
    time.sleep(5)

    # Genera traffico con nping
    generate_nping_traffic(target_ip)
    time.sleep(5)

    # Genera ping flood
    generate_ping_flood(target_ip)
    time.sleep(5)

    # Genera scansione nmap
    generate_nmap_scan(target_ip)
    time.sleep(5)

    # Genera traffico con Scapy
    generate_scapy_traffic(target_ip)
    time.sleep(5)

    print("Traffic generation completed.")
