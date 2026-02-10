import socket, json, threading, time, psutil, platform, os
from security_manager import SecurityManager
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from remote_control import mover_mouse, clicar, pressionar_tecla

DISCOVERY_PORT = 50000
TCP_PORT = 50001

class ClienteAgente:
    def __init__(self):
        self.sec = SecurityManager("Cliente")
        self.running = True

    def coletar_dados(self):
        interfaces = []
        for nome, addrs in psutil.net_if_addrs().items():
            stats = psutil.net_if_stats().get(nome)
            ip = next((a.address for a in addrs if a.family == socket.AF_INET), "N/A")

            if nome == "lo":
                tipo = "LOOPBACK"
            elif "wlan" in nome.lower() or "wi-fi" in nome.lower():
                tipo = "WIFI"
            else:
                tipo = "ETHERNET"

            interfaces.append({
                "nome": nome,
                "ip": ip,
                "status": "UP" if stats and stats.isup else "DOWN",
                "tipo": tipo
            })

        return {
            "so": f"{platform.system()} {platform.release()}",
            "cpus": psutil.cpu_count(logical=False),
            "ram_livre_gb": round(psutil.virtual_memory().available / (1024**3), 2),
            "disco_livre_gb": round(psutil.disk_usage('/').free / (1024**3), 2),
            "interfaces": interfaces
        }

    def tcp_server(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("0.0.0.0", TCP_PORT))
        sock.listen(5)
        while self.running:
            conn, _ = sock.accept()
            threading.Thread(target=self.handle_server, args=(conn,), daemon=True).start()

    def handle_server(self, conn):
        try:
            conn.sendall(self.sec.public_bytes())
            server_pub = conn.recv(4096)

            enc_key = conn.recv(512)
            aes_key = self.sec.decrypt_key(enc_key)
            aes = AESGCM(aes_key)

            nonce = conn.recv(12)
            data = conn.recv(4096)
            request = json.loads(aes.decrypt(nonce, data, None))

            cmd = request.get("type")

            if cmd == "GET_STATS":
                payload = json.dumps(self.coletar_dados()).encode()

            elif cmd == "MOUSE_MOVE":
                mover_mouse(request["direction"])
                payload = b'{"status":"OK"}'

            elif cmd == "MOUSE_CLICK":
                clicar(request.get("button", "LEFT"))
                payload = b'{"status":"OK"}'

            elif cmd == "KEY_PRESS":
                pressionar_tecla(request["key"])
                payload = b'{"status":"OK"}'

            else:
                payload = b'{"status":"UNKNOWN_COMMAND"}'
            
            n = os.urandom(12)
            conn.sendall(n + aes.encrypt(n, payload, None))
        except:
            pass
        finally:
            conn.close()

    def discovery(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        while self.running:
            msg = f"HELLO:{TCP_PORT}".encode()
            sock.sendto(msg, ("<broadcast>", DISCOVERY_PORT))
            time.sleep(10)

if __name__ == "__main__":
    cliente = ClienteAgente()
    threading.Thread(target=cliente.discovery, daemon=True).start()
    print("Cliente ativo...")
    cliente.tcp_server()
