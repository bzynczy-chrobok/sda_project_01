import netifaces


def get_all_interfaces() -> list:
    """
    Funkcja zwracająca listę interfejsów w systemie.
    :return: list
    """
    # print(netifaces.interfaces())
    return netifaces.interfaces()


def get_available_interfaces() -> list:
    """
    Funkcja zwracająca listę interfejsów które mają przypisany broadcast.
    Lista wszystkich interfejsów pobierana jest za pośrednictwem get_all_interfaces
    :return: list
    """
    interfaces = get_all_interfaces()
    response = []
    for ifc in interfaces:
        if netifaces.AF_INET in netifaces.ifaddresses(ifc): #vboxnet0 nie posiada takiego klucza
            broadcast = netifaces.ifaddresses(ifc)[netifaces.AF_INET][0].get('broadcast')
            if broadcast:
                response.append(ifc)
    # print(response)
    return response


def get_ip_address(interface: str) -> str:
    """
    Funkcja zwracająca adres ip przekazanego w argumencie wywołania interfejsu
    :param interface: str
    :return: str
    """
    return netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']


def get_netmask(interface: str) -> str:
    """
    Funkcja zwracająca maskę podsieci przypisaną do przekazanego w argumencie interfejsu.
    :param interface: str
    :return: str
    """
    return netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['netmask']


if __name__ == "__main__":
    for interface in get_available_interfaces():
        print(f"Interfejs: {interface}")
        print(f"IP: {get_ip_address(interface)}")
        print(f"Maska sieci: {get_netmask(interface)}")
        print('---------------------------')
