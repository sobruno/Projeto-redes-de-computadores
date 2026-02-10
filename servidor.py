import socket, threading, time, json, os, csv
from security_manager import SecurityManager
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

DISCOVERY_PORT = 50000
AUTHORIZED_CLIENTS = []  # fingerprints permitidos

class ServidorMonitor:
    def __init__(self):
        self.sec = SecurityManager("Servidor")
        self.clients = {}
        self.audit = "audit_log.txt"

    def log(self, msg):
        with open(self.audit, "a") as f:
            f.write(f"[{time.ctime()}] {msg}\n")

    def listen_discovery(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("0.0.0.0", DISCOVERY_PORT))
        while True:
            data, addr = sock.recvfrom(1024)
            port = int(data.decode().split(":")[1])
            self.clients[addr[0]] = {
                "port": port,
                "last_seen": time.time(),
                "data": {}
            }

    def fetch_data(self, ip, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, port))

            client_pub = sock.recv(4096)
            fingerprint = self.sec.fingerprint(client_pub)

            if AUTHORIZED_CLIENTS and fingerprint not in AUTHORIZED_CLIENTS:
                self.log(f"Acesso negado: {ip}")
                sock.close()
                return

            sock.sendall(self.sec.public_bytes())
            aes_key = os.urandom(32)
            sock.sendall(self.sec.encrypt_key(aes_key, client_pub))
            aes = AESGCM(aes_key)

            nonce = os.urandom(12)
            request = json.dumps({"type": "GET_STATS"}).encode()
            sock.sendall(nonce + aes.encrypt(nonce, request, None))

            r_nonce = sock.recv(12)
            r_data = sock.recv(4096)
            self.clients[ip]["data"] = json.loads(aes.decrypt(r_nonce, r_data, None))
            self.clients[ip]["last_seen"] = time.time()
            self.log(f"Dados atualizados: {ip}")
        except:
            self.log(f"Erro ao acessar {ip}")

    def media_ram(self):
        ativos = [c for c in self.clients.values() if time.time() - c["last_seen"] < 30]
        if not ativos:
            return 0
        return sum(c["data"].get("ram_livre_gb", 0) for c in ativos) / len(ativos)

    def exportar(self, formato="csv"):
        if formato == "csv":
            with open("relatorio.csv", "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["IP", "SO", "RAM Livre", "Disco Livre"])
                for ip, c in self.clients.items():
                    d = c["data"]
                    writer.writerow([ip, d.get("so"), d.get("ram_livre_gb"), d.get("disco_livre_gb")])
        else:
            with open("relatorio.json", "w") as f:
                json.dump(self.clients, f, indent=4)

    def detalhar_cliente(self, ip):
        cliente = self.clients.get(ip)

        if not cliente:
            print("Cliente não encontrado.")
            return

        # 🔹 Se não tiver dados, busca automaticamente
        if not cliente.get("data"):
            print("Buscando dados do cliente...")
            self.fetch_data(ip, cliente["port"])
            time.sleep(1)

        data = cliente.get("data")
        if not data:
            print("Cliente não respondeu com dados.")
            return

        status = "ONLINE" if time.time() - cliente["last_seen"] < 30 else "OFFLINE"

        print("\n===== DETALHES DO CLIENTE =====")
        print(f"IP: {ip}")
        print(f"Status: {status}")
        print(f"Sistema Operacional: {data.get('so')}")
        print(f"CPUs (núcleos físicos): {data.get('cpus')}")
        print(f"RAM Livre: {data.get('ram_livre_gb')} GB")
        print(f"Disco Livre: {data.get('disco_livre_gb')} GB")

        print("\nInterfaces de Rede:")
        for iface in data.get("interfaces", []):
            print(
                f"- {iface['nome']} | IP: {iface['ip']} | "
                f"Status: {iface['status']} | Tipo: {iface['tipo']}"
            )

            
    def enviar_comando(self, ip, port, comando):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, port))

            client_pub = sock.recv(4096)
            sock.sendall(self.sec.public_bytes())

            aes_key = os.urandom(32)
            sock.sendall(self.sec.encrypt_key(aes_key, client_pub))
            aes = AESGCM(aes_key)

            nonce = os.urandom(12)
            sock.sendall(nonce + aes.encrypt(nonce, json.dumps(comando).encode(), None))

            sock.close()
            self.log(f"Comando enviado para {ip}: {comando}")

        except Exception as e:
            self.log(f"Erro comando remoto {ip}: {e}")

    def menu(self):
        while True:
            print(f"\nClientes: {len(self.clients)} | Média RAM Livre: {self.media_ram():.2f} GB")
            print("1 - Listar clientes")
            print("2 - Atualizar dados dos clientes")
            print("3 - Exportar CSV")
            print("4 - Detalhar cliente")
            print("5 - Sair")
            print("6 - Controle Remoto")

            op = input("> ")

            if op == "1":
                for ip, c in self.clients.items():
                    status = "ONLINE" if time.time() - c["last_seen"] < 30 else "OFFLINE"
                    print(ip, status)

            elif op == "2":
                for ip, c in self.clients.items():
                    threading.Thread(
                        target=self.fetch_data,
                        args=(ip, c["port"]),
                        daemon=True
                    ).start()

            elif op == "3":
                self.exportar()
                print("Relatório exportado.")

            elif op == "4":
                ip = input("Digite o IP do cliente: ")
                self.detalhar_cliente(ip)

            elif op == "5":
                break

            elif op == "6":
                ip = input("IP do cliente: ")

                if ip not in self.clients:
                    print("Cliente não encontrado.")
                    return

                print("1 - Mouse UP")
                print("2 - Mouse DOWN")
                print("3 - Mouse LEFT")
                print("4 - Mouse RIGHT")
                print("5 - Click esquerdo")
                print("6 - Pressionar tecla")

                c = input("> ")

                if c == "1":
                    self.enviar_comando(
                        ip, self.clients[ip]["port"],
                        {"type": "MOUSE_MOVE", "direction": "UP"}
                    )

                elif c == "2":
                    self.enviar_comando(
                        ip, self.clients[ip]["port"],
                        {"type": "MOUSE_MOVE", "direction": "DOWN"}
                    )

                elif c == "3":
                    self.enviar_comando(
                        ip, self.clients[ip]["port"],
                        {"type": "MOUSE_MOVE", "direction": "LEFT"}
                    )

                elif c == "4":
                    self.enviar_comando(
                        ip, self.clients[ip]["port"],
                        {"type": "MOUSE_MOVE", "direction": "RIGHT"}
                    )

                elif c == "5":
                    self.enviar_comando(
                        ip, self.clients[ip]["port"],
                        {"type": "MOUSE_CLICK", "button": "LEFT"}
                    )

                elif c == "6":
                    tecla = input("Digite a tecla: ")
                    self.enviar_comando(
                        ip, self.clients[ip]["port"],
                        {"type": "KEY_PRESS", "key": tecla}
                    )

                else:
                    print("Opção inválida.")

if __name__ == "__main__":
    s = ServidorMonitor()
    threading.Thread(target=s.listen_discovery, daemon=True).start()
    s.menu()
