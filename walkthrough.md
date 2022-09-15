# Przewodnik rozwiązania zadań
___
## Podstawowa konfiguracja
- maszyna wirtualna z systemem kali
- maszyna wirtualna SDA\
Sieć izolowana typu host-only 
___
## Ustalić własny adres IP wraz z maską podsieci

**skrypt**: [network_info_final.py](network_info_final.py) wywołany bez argumentów.

```console
kali@kali:~$ python network_info_final.py
Interfejs: eth0
IP: 192.168.56.100
Maska sieci: 255.255.255.0
---------------------------
```

**Opis działania**: Skrypt robi pętlę po wykrytych w systemie interfejsach i zwraca adres IP przypisany do aktualnie iterowanego interfejsu.
___
## Na podstawie powyższych informacji przeskanować sieć i ustalić adres IP celu.
**skrypt**: [port_scanner_final.py](port_scanner_final.py) wywołany bez argumentów.

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
**Opis działania**: Skrypt korzysta z poprzednio opisanego skrytpu. Na podstawie otrzymanej listy interfejsów do robi pętlę po nich i wykonuje skanowanie hostów zgodnie z maską sieciewią. Domyślnie skrypt nie wyświetla wyników skanowania portów na własnym IP.