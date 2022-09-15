from ipaddress import IPv4Network
import nmap
import network_info_final as network_info # w tym miejscu importujemy sobie wcześniej stworzony skrypt do określania ip i maski


#####################################################################################
# na kali: pip install python-nmap
# żeby sprawdzać wyniki w pycharm też pip install albo przez zakładkę python packages
# korzystam z: https://pypi.org/project/python-nmap/
#####################################################################################

def get_netmask_bits(netmask: str) -> int:
    """
    Funkcja zwracająca maskę podsieci w reprezentacji bitowej
    :param netmask: str
    :return: int
    """
    # w nmap maskę sieci musimy podać w postaci /24 jeżeli równa się ona: 255.255.255.0
    # musimy dokonać jej konwersji i możemy to zrobić na kilka sposobów
    # Robię przykład z użyciem biblioteki ipaddress i bez użycia bibliotek
    # Podejmiemy decyzję, którą wersję zostawimy w końcowym skrypcie

    # z biblioteką
    netmask_bits = IPv4Network("0.0.0.0/" + netmask).prefixlen

    # bez biblioteki
    # netmask_bits = sum(bin(int(x)).count('1') for x in netmask.split('.'))

    return netmask_bits


def scan_my_network(interface_name: str, ports: str = "1-100", ip=None, scan_yourself: str = False) -> list:
    """
    Funkcja zwracająca listę słowników zawierających informacje o wyniku skanowania
    :param interface_name: str
    :param ports: str
    :param ip: None or str - w przypadku None, skanowanie podsieci
    :param scan_yourself: bool - Jeżeli jest False, to w przypadku skanowania sieci, ten host nie pojawi się w wynikach
    :return: list
    """
    results = []
    print("#" * 40)
    if not ip:
        # nie przekazano ip - będziemy skanować całą podsieć
        my_ip = network_info.get_ip_address(interface_name)
        print("# Skanuję sieć w poszukiwaniu hostów.  #")

    else:
        my_ip = ip
        print(f"# Skanuję {my_ip}" + ' ' * (29 - len(my_ip)) + "#")

    my_netmask = network_info.get_netmask(interface_name)
    my_netmask_bits = get_netmask_bits(my_netmask)
    scan_address = my_ip

    print(f"# Interfejs: {interface_name}" + ' ' * (26 - len(interface_name)) + "#")
    print(f"# Ip: {my_ip}" + ' ' * (33 - len(my_ip)) + "#")
    if not ip and not scan_yourself:
        print(f"# Pomijam siebie!" + ' ' * 22 + "#")
    print("#" * 40)
    if not ip:
        scan_address = scan_address + '/' + str(my_netmask_bits)

    nm = nmap.PortScanner()
    nm.scan(scan_address, ports)

    for host in nm.all_hosts():
        if not ip and not scan_yourself and host == my_ip:
            continue
        result = {
            host: {}
        }
        print('---------------------')
        print(f"IP: {host}")
        print(f"Nazwa hosta: {nm[host].hostname()}")
        print(f"Status: {nm[host].state()}")
        # print(nm[host].all_protocols())
        if len(nm[host].all_protocols()) > 0:
            print("Protokoły ┐")
        for proto in nm[host].all_protocols():
            print(f"          └ {proto.upper()} ┐")

            lport = nm[host][proto].keys()
            result[host]['ports'] = []
            for port in lport:
                result_port = {
                    'port': port,
                    'state': nm[host][proto][port]['state']
                }
                result[host]['ports'].append(result_port)
                print(f"                ┌ Port: {port}, status: {nm[host][proto][port]['state']}")
                if nm[host][proto][port]['product'] != '':
                    print(f"                └ {nm[host][proto][port]['product']} {nm[host][proto][port]['version']} {nm[host][proto][port]['extrainfo']}")
                else:
                    print(
                        f"                └ Usługa na tym porcie się nie przedstawiła!")
            results.append(result)
    return results


if __name__ == "__main__":
    import argparse
    descr = "Prosty skaner portów wybranej maszyny.\nMoże skanować całą sieć, jak i pojedynczą maszynę."
    parser = argparse.ArgumentParser(description="Skaner portów.")
    parser.add_argument("-H", "--host", help="Nazwa hosta albo adres IP.")
    parser.add_argument("-P", "--port", help="Port lub zakres skanowanych portów. W przypadku zakresu wpisz np 1-80")
    interfaces = network_info.get_available_interfaces()

    # parsowanie przekazanych argumentów
    args = parser.parse_args()
    if args.host:
        # skrypt uruchomiony z argumentem (adresem ip skanowanej maszyny)
        ip = args.host
    else:
        # Skrypt uruchomiony bez argumentu ip. Przechodę w tryb skanowania sieci na podstawie wykrytego automatycznie adresu ip
        ip = None
    if args.port:
        port = args.port
    else:
        port = None

    for interface in interfaces:
        scan_my_network(interface_name=interface, ip=ip, ports=port)
