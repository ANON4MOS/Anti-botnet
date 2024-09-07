import subprocess
import pyfiglet
from termcolor import colored
import os

def clear_terminal():
    
    command = 'cls' if os.name == 'nt' else 'clear'
    subprocess.run([command], shell=True)

def print_banner():
    clear_terminal()  
    
    banner_text = "Anti - botnet"
    banner = pyfiglet.figlet_format(banner_text, font="standard")
    author_text = "Autor: 100CONTA"
    
    combined_banner = banner + '\n' + author_text

    lines = combined_banner.splitlines()
    colored_lines = [colored(line[:29], 'red') + line[29:] if i < len(banner.splitlines()) else line for i, line in enumerate(lines)]
    full_banner = "\n".join(colored_lines)

    print(full_banner)

def block_ips_from_file(file_path):
    if not os.path.exists(file_path):
        print("Arquivo especificado não encontrado. Usando lista padrão.")
        file_path = 'lista.txt'
        
    with open(file_path, 'r') as file:
        ip_list = file.readlines()

    ip_list = [ip.strip() for ip in ip_list if ip.strip()]

    for ip in ip_list:
        try:
            subprocess.run(['sudo', 'iptables', '-A', 'INPUT', '-s', ip, '-j', 'REJECT'], check=True)
            print(f"IP {ip} rejeitado com sucesso na cadeia INPUT.")
        except subprocess.CalledProcessError as e:
            print(f"Erro ao rejeitar o IP {ip} na cadeia INPUT: {e}")

if __name__ == "__main__":
    print_banner()
    file_path = input("Digite o caminho para a lista de IPs (pressione Enter para usar a lista padrão): ")
    file_path = file_path.strip() if file_path else 'lista.txt'
    block_ips_from_file(file_path)
