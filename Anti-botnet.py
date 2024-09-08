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

def find_malformed_dns(pcap_file):
    malformed_ips_file = 'malformed_dns_ips.txt'
    try:
        subprocess.run(['tshark', '-r', pcap_file, '-Y', 'dns.flags.rcode == 1', '-T', 'fields', '-e', 'ip.src', '-e', 'ip.dst'], check=True, stdout=open(malformed_ips_file, 'w'))
        print(f"IPs com DNS malformados foram salvos em {malformed_ips_file}")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao analisar o arquivo .pcap para DNS malformado: {e}")

def protocol_menu(pcap_file):
    while True:
        clear_terminal()
        print_banner()
        print("Qual Protocolo você deseja verificar?")
        print("[1] Malformed DNS")
        print("[0] Voltar ao menu principal")

        option = input("Digite sua escolha: ").strip()

        if option == '1':
            find_malformed_dns(pcap_file)
        elif option == '0':
            break
        else:
            print("Opção inválida, tente novamente.")
        
        input("\nPressione Enter para voltar ao menu de protocolos...")

def main_menu():
    while True:
        clear_terminal()
        print_banner()
        print("O que você deseja fazer?")
        print("[1] Bloquear uma lista de IPs")
        print("[2] Verificar um arquivo pcap em busca de IPs malformados")
        print("[0] Sair")

        option = input("Digite sua escolha: ").strip()

        if option == '1':
            use_blackhole = input("Deseja redirecionar os IPs para a blackhole? (s/n): ").strip().lower() == 's'
            file_path = input("Digite o caminho para a lista de IPs (pressione Enter para usar a lista padrão): ")
            file_path = file_path.strip() if file_path else 'lista.txt'
            block_ips_from_file(file_path, use_blackhole)
        elif option == '2':
            pcap_file = input("Digite o caminho para o arquivo .pcap: ").strip()
            if os.path.exists(pcap_file):
                protocol_menu(pcap_file)
            else:
                print("Arquivo .pcap não encontrado.")
        elif option == '0':
            print("Saindo...")
            break
        else:
            print("Opção inválida, tente novamente.")
        
        input("\nPressione Enter para voltar ao menu...")

if __name__ == "__main__":
    main_menu()
