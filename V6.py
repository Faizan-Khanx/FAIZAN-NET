import ipaddress
import csv
import json
from termcolor import colored

def display_logo() -> None:
    red = "\033[31m"
    purple = "\033[35m"
    cyan = "\033[36m"
    reset = "\033[0m"

    print("\033[H\033[2J\033[1m\033[36m                                                        ")
    print(f"{red}███████╗ █████╗ ██╗███████╗ █████╗ ███╗   ██╗    ███╗   ██╗███████╗████████╗{reset}")
    print(f"{red}██╔════╝██╔══██╗██║╚══███╔╝██╔══██╗████╗  ██║    ████╗  ██║██╔════╝╚══██╔══╝{reset}")
    print(f"{red}█████╗  ███████║██║  ███╔╝ ███████║██╔██╗ ██║    ██╔██╗ ██║█████╗     ██║   {reset}")
    print(f"{red}██╔══╝  ██╔══██║██║ ███╔╝  ██╔══██║██║╚██╗██║    ██║╚██╗██║██╔══╝     ██║   {reset}")
    print(f"{red}██║     ██║  ██║██║███████╗██║  ██║██║ ╚████║    ██║ ╚████║███████╗   ██║   {reset}")
    print(f"{red}╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝    ╚═╝  ╚═══╝╚══════╝   ╚═╝   {reset}")
    print(f"{purple}                        MADE BY FAIZAN KHAN \n              INSTAGRAM: @EthicalFaizan GITHUB: @Faizan-Khanx {reset}")

def get_network(ip: str, cidr: str) -> ipaddress.IPv6Network:
    try:
        net = ipaddress.ip_network(f"{ip}/{cidr}", strict=False)
        return net
    except ValueError:
        print(colored("\n[!] Invalid IPv6 Address or CIDR!\n", 'red'))
        exit(1)

def export_data(network: ipaddress.IPv6Network, export_format: str) -> None:
    data = {
        'IPv6 Address': str(network.network_address.exploded),
        'Prefix Length': f"/{network.prefixlen}",
        'Broadcast Address': str(network.broadcast_address.exploded),
        'Host Range Start': str(network.network_address.exploded),
        'Host Range End': str(network.broadcast_address.exploded),
        'Total Number of Hosts': network.num_addresses
    }

    if export_format == 'csv':
        with open('FaizanNetV6.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([colored('Subnet Calculation Details', 'cyan')])
            writer.writerow([colored('===============================', 'cyan')])
            for key, value in data.items():
                writer.writerow([colored(f"{key}: {value}", 'yellow')])
            writer.writerow([colored('===============================', 'cyan')])
        print(colored("\nSubnet details exported to 'FaizanNetV6.csv'", 'green'))
    
    elif export_format == 'json':
        with open('FaizanNetV6.json', 'w') as file:
            json.dump(data, file, indent=4)
        print(colored("\nSubnet details exported to 'FaizanNetV6.json'", 'green'))

def visual_representation_ipv6(network: ipaddress.IPv6Network) -> None:
    print(colored("\nVisual Representation of Subnetting (IPv6):", 'cyan'))
    print(colored(f"Network: {network}", 'cyan'))
    print(colored(f"Total Hosts: {network.num_addresses}", 'cyan'))

# Main function to get IP and CIDR at runtime and calculate subnet details
def main() -> None:
    display_logo()

    ip = input(colored("\n[?] Enter an IPv6 Address (with or without CIDR): ", 'cyan'))
    cidr = input(colored("[?] Enter a CIDR prefix (Example: 64): ", 'cyan')).strip('/')

    net = get_network(ip, cidr)
    
    print(colored("\nSubnet Details:", 'cyan'))
    print(colored(f"IPv6 Address: {net.network_address.exploded}", 'cyan'))
    print(colored(f"Prefix Length: /{net.prefixlen}", 'cyan'))
    print(colored(f"Host Range: {net.network_address.exploded} - {net.broadcast_address.exploded}", 'cyan'))
    print(colored(f"Total Hosts: {net.num_addresses}", 'cyan'))
    
    visual_representation_ipv6(net)
    
    export = input(colored("\n[?] Do you want to export the details? (yes/no): ", 'cyan')).strip().lower()
    if export in ['yes', 'y']:
        print(colored("\n1. CSV\n2. JSON", 'red'))
        export_choice = input(colored("[?] Choose export format (1 or 2): ", 'cyan')).strip()
        if export_choice == '1':
            export_data(net, 'csv')
        elif export_choice == '2':
            export_data(net, 'json')
        else:
            print(colored("[!] Invalid option. Export aborted.", 'red'))

if __name__ == '__main__':
    main()

