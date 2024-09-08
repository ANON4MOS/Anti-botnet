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

def route_exists(ip):
    try:
        result = subprocess.run(['ip', 'route', 'show', ip], capture_output=True, text=True)
        return ip in result.stdout
    except subprocess.CalledProcessError:
        return False

def block_ips_from_file(file_path, use_blackhole):
    if not os.path.exists(file_path):
        print("Arquivo especificado não encontrado. Usando lista padrão.")
        file_path = 'lista.txt'
        
    with open(file_path, 'r') as file:
        ip_list = file.readlines()

    ip_list = [ip.strip() for ip in ip_list if ip.strip()]

    for ip in ip_list:
        try:
            subprocess.run(['sudo', 'iptables', '-A', 'INPUT', '-s', ip, '-j', 'REJECT'], check=True)
            print(f"IP {ip} rejeitado com sucesso")
            
            if use_blackhole:
                if not route_exists(ip):
                    subprocess.run(['sudo', 'ip', 'route', 'add', 'blackhole', ip], check=True)
                    print(f"IP {ip} redirecionado para a blackhole com sucesso.")
                else:
                    print(f"Rota para {ip} já existe. Ignorando.")
            
        except subprocess.CalledProcessError as e:
            print(f"Erro ao processar o IP {ip}: {e}")

if __name__ == "__main__":
    print_banner()
    
    use_blackhole = input("Deseja redirecionar os IPs para a blackhole? (s/n): ").strip().lower() == 's'
    
    file_path = input("Digite o caminho para a lista de IPs (pressione Enter para usar a lista padrão): ")
    file_path = file_path.strip() if file_path else 'lista.txt'
    
    block_ips_from_file(file_path, use_blackhole)
