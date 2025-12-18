import requests
from requests.auth import HTTPBasicAuth
import socket
import threading

# Konfiguracja
base_ip = "192.168.0."  # zmień jeśli masz inną podsieć
ports = [80, 8080, 8000]
credentials = [
    ("admin", "admin"),
    ("admin", "1234"),
    ("admin", ""),
    ("root", "root"),
    ("user", "user"),
    ("admin", "password"),
    ("admin", "pass"),
    ("root", "admin")
]

# Główna funkcja testująca jedno IP
def scan_ip(ip):
    for port in ports:
        try:
            sock = socket.socket()
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            sock.close()

            if result == 0:
                url = f"http://{ip}:{port}/"
                print(f"🌐 Znaleziono port {port} otwarty na {ip}")

                for login, password in credentials:
                    try:
                        r = requests.get(url, auth=HTTPBasicAuth(login, password), timeout=3)
                        if r.status_code == 200:
                            print(f"✅ DOSTĘP ZNALEZIONY: IP={ip}, PORT={port}, LOGIN={login}, HASŁO={password}")
                            return  # opcjonalnie break, jeśli chcesz testować dalej
                        elif r.status_code == 401:
                            pass  # nieudane logowanie
                    except:
                        pass
        except:
            pass

# Wielowątkowe skanowanie IP w sieci
threads = []
for i in range(1, 255):
    ip = base_ip + str(i)
    t = threading.Thread(target=scan_ip, args=(ip,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print("✅ Skanowanie zakończone.")
