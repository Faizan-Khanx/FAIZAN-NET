import ipaddress
import argparse
import csv
import json
import socket
import nmap
from typing import Tuple, List, Union

# Create the parser
parser = argparse.ArgumentParser(description='SubnetWizard')

# Add the arguments
ip_help = "The IP address to calculate (IPv4/IPv6)\nExample: 192.168.0.100/24 or 2001:db8::/64\nSupports both CIDR and Subnet Mask"
parser.add_argument('-i', dest='ip', type=str, help=ip_help)
subnet_help = "The netmask to subnet (optional)\nExample: 255.255.255.0 or /24"
parser.add_argument('-s', dest='subnet', type=str, help=subnet_help)
export_help = "Export the subnet details to a CSV or JSON file"
parser.add_argument('-e', dest='export', type=str, help=export_help, choices=['csv', 'json'])
version_help = "Select IP version (IPv4 or IPv6)"
parser.add_argument('-v', dest='version', type=str, choices=['ipv4', 'ipv6'], default='ipv4', help=version_help)

def display_logo() -> None:
    red = "\033[31m"
    purple = "\033[35m"
    reset = "\033[0m"
    
    print("\033[H\033[2J\033[1m\033[36m                                                        ")
    print(f"{red}███████╗ █████╗ ██╗███████╗ █████╗ ███╗   ██╗    ███╗   ██╗███████╗████████╗{reset}")
    print(f"{red}██╔════╝██╔══██╗██║╚══███╔╝██╔══██╗████╗  ██║    ████╗  ██║██╔════╝╚══██╔══╝{reset}")
    print(f"{red}█████╗  ███████║██║  ███╔╝ ███████║██╔██╗ ██║    ██╔██╗ ██║█████╗     ██║   {reset}")
    print(f"{red}██╔══╝  ██╔══██║██║ ███╔╝  ██╔══██║██║╚██╗██║    ██║╚██╗██║██╔══╝     ██║   {reset}")
    print(f"{red}██║     ██║  ██║██║███████╗██║  ██║██║ ╚████║    ██║ ╚████║███████╗   ██║   {reset}")
    print(f"{red}╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝    ╚═╝  ╚═══╝╚══════╝   ╚═╝   {reset}")
    print(f"{purple}                        MADE BY FAIZAN KHAN \n              INSTAGRAM: @EthicalFaizan GITHUB: @Faizan-Khanx {reset}")

def get_network(ip: str = None) -> Tuple[ipaddress._BaseNetwork, str]:
    if ip:
        try:
            if ip.count("/") == 0: ip += "/24"  # Default mask for IPv4
            net = ipaddress.ip_network(ip, strict=False)
            ip = ip.split("/")[0]
            return (net, ip)
        except ValueError:
            print("\n\033[36m[\033[31m!\033[36m]\033[0m Invalid IP Address!\n")
            exit(1)
    print()
    while True:
        try:
            in_ = input("\033[36m[\033[31m?\033[36m]\033[0m Enter an IP Address (IPv4/IPv6 with CIDR): \033[36m")
            if in_ == "": in_ = "192.168.0.100/24"  # Default IPv4
            if in_.count("/") == 0: in_ += "/24"  # Default mask for IPv4
            net = ipaddress.ip_network(in_, strict=False)
            ip = in_.split("/")[0]
            return (net, ip)
        except ValueError:
            print("\n\033[36m[\033[31m!\033[36m]\033[0m Invalid IP Address!\n")
            continue

def get_subnet(subnet: str = None) -> str:
    if subnet:
        if subnet == "0": 
            print("\n\033[36m[\033[31m!\033[36m]\033[0m Invalid Netmask!\n")
            exit(1)
        try:
            net = ipaddress.ip_network(f"10.0.0.0/{subnet}", strict=False)
            return net.prefixlen
        except ValueError:
            print("\n\033[36m[\033[31m!\033[36m]\033[0m Invalid Netmask!\n")
            exit(1)
    print()
    while True:
        try:
            in_ = input("\033[36m[\033[31m?\033[36m]\033[0m Enter a Netmask to subnet (optional): \033[36m")
            if in_ == "0": 
                print("\n\033[36m[\033[31m!\033[36m]\033[0m Invalid Netmask!\n")
                continue
            if in_ == "": return None
            net = ipaddress.ip_network(f"10.0.0.0/{in_.strip('/')}", strict=False)
            return net.prefixlen
        except ValueError:
            print("\n\033[36m[\033[31m!\033[36m]\033[0m Invalid Netmask!\n")
            continue

def export_data(network: Union[ipaddress.IPv4Network, ipaddress.IPv6Network], export_format: str) -> None:
    data = {
        'IP Address': str(network.network_address),
        'Netmask': str(network.netmask),
        'CIDR': f"/{network.prefixlen}",
        'Broadcast Address': str(network.broadcast_address),
        'Host Range': f"{network.network_address} - {network.broadcast_address}",
        'Hosts': network.num_addresses
    }

    if export_format == 'csv':
        with open('subnet_details.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data.keys())
            writer.writerow(data.values())
        print("\033[36mSubnet details exported to 'subnet_details.csv'\033[0m")
    elif export_format == 'json':
        with open('subnet_details.json', 'w') as file:
            json.dump(data, file, indent=4)
        print("\033[36mSubnet details exported to 'subnet_details.json'\033[0m")

def classify_network(ip: str) -> str:
    first_octet = int(ip.split('.')[0])
    if 0 <= first_octet < 128:
        return "Class A"
    elif 128 <= first_octet < 192:
        return "Class B"
    elif 192 <= first_octet < 224:
        return "Class C"
    elif 224 <= first_octet < 240:
        return "Class D (Multicast)"
    else:
        return "Class E (Experimental)"

def host_status(ip: str) -> str:
    """Check if a host is up or down.""" 
    try:
        socket.gethostbyaddr(ip)
        return "UP"
    except socket.herror:
        return "DOWN"

def scan_ports_and_os(ip: str) -> Tuple[List[str], str]:
    """Scan for open ports and OS information."""
    nm = nmap.PortScanner()
    try:
        nm.scan(ip, arguments='-O')
        open_ports = [port for port in nm[ip]['tcp'].keys() if nm[ip]['tcp'][port]['state'] == 'open']
        os_info = nm[ip].get('osclass', [{'osclass': 'Unknown'}])[0].get('osclass', 'Unknown')
        return open_ports, os_info
    except Exception as e:
        print(f"\033[36m[\033[31m!\033[36m]\033[0m Error scanning {ip}: {e}")
        return [], "Unknown"

def visual_representation_ipv4(network: ipaddress.IPv4Network) -> None:
    hosts = list(network.hosts())
    total_hosts = network.num_addresses
    print("\n\033[0mVisual Representation of Subnetting (IPv4):\n")
    print("Network: \033[36m{}\033[0m".format(network))
    print("Total Hosts: \033[36m{}\033[0m".format(total_hosts))
    if hosts:
        print("IP Range: \033[36m{} - {}\033[0m\n".format(hosts[0], hosts[-1]))

        # Header with colors
        header = "{:<18} | {:<40} | {:<7} | {:<40} | {:<40} | {:<25} | {:<25}".format(
            "Host", "Binary Representation", "Status", "Network Binary", "Netmask Binary", "Ports", "OS Info"
        )
        print("\033[1;34m" + header + "\033[0m")
        print("-" * len(header))  # Line length to match header width

        network_bin = '.'.join(bin(int(x))[2:].zfill(8) for x in str(network.network_address).split('.'))
        netmask_bin = '.'.join(bin(int(x))[2:].zfill(8) for x in str(network.netmask).split('.'))
        
        for host in hosts:
            binary_host = '.'.join(bin(int(x))[2:].zfill(8) for x in str(host).split('.'))
            status = host_status(str(host))
            status_color = "\033[32m" if status == "UP" else "\033[31m"
            open_ports, os_info = scan_ports_and_os(str(host))
            ports = ', '.join(map(str, open_ports)) if open_ports else "None"
            print("{:<18} | {:<40} | {}{:<7}\033[0m | {:<40} | {:<40} | {:<25} | {:<25}".format(
                str(host), binary_host, status_color, status, network_bin, netmask_bin, ports, os_info
            ))

def visual_representation_ipv6(network: ipaddress.IPv6Network) -> None:
    print("\n\033[0mVisual Representation of Subnetting (IPv6):\n")
    print("Network: \033[36m{}\033[0m".format(network))
    print("Total Hosts: \033[36m{}\033[0m".format(network.num_addresses))

# Main function to parse arguments and call appropriate functions
def main() -> None:
    args = parser.parse_args()
    
    display_logo()
    
    net, ip = get_network(args.ip)
    subnet_prefix = get_subnet(args.subnet)
    
    if subnet_prefix:
        net = ipaddress.ip_network(f"{net.network_address}/{subnet_prefix}", strict=False)
    
    print("\n\033[36mSubnet Details:\033[0m")
    print(f"IP Address: \033[36m{net.network_address}\033[0m")
    print(f"Netmask: \033[36m{net.netmask}\033[0m")
    print(f"CIDR: \033[36m/{net.prefixlen}\033[0m")
    print(f"Broadcast Address: \033[36m{net.broadcast_address}\033[0m")
    print(f"Host Range: \033[36m{net.network_address} - {net.broadcast_address}\033[0m")
    print(f"Total Hosts: \033[36m{net.num_addresses}\033[0m")
    print(f"Network Class: \033[36m{classify_network(str(net.network_address))}\033[0m")

    if args.version == 'ipv4':
        visual_representation_ipv4(net)
    else:
        visual_representation_ipv6(net)
    
    if args.export:
        export_data(net, args.export)

if __name__ == '__main__':
    main()

