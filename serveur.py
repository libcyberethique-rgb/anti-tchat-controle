import socket
import threading

HOST = '0.0.0.0'  # Écoute sur toutes les interfaces locales
PORT = 50000

clients = []
pseudo_map = {}

def broadcast(message, sender_socket=None):
    """Envoie un message à tous les clients connectés."""
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                client.close()
                if client in clients:
                    clients.remove(client)

def handle_client(client_socket):
    """Gère la réception des messages d'un client."""
    try:
        # Premier message reçu = le pseudo
        pseudo = client_socket.recv(1024).decode('utf-8')
        pseudo_map[client_socket] = pseudo
        
        msg_bienvenue = f"*** {pseudo} a rejoint le tchat ! ***"
        print(msg_bienvenue)
        broadcast(msg_bienvenue.encode('utf-8'))

        while True:
            msg = client_socket.recv(1024)
            if not msg:
                break
            # Renvoie le message formaté : "Pseudo: message"
            texte_complet = f"{pseudo}: {msg.decode('utf-8')}"
            broadcast(texte_complet.encode('utf-8'), client_socket)
            
    except:
        pass
    finally:
        if client_socket in clients:
            clients.remove(client_socket)
            pseudo = pseudo_map.get(client_socket, "Un utilisateur")
            msg_depart = f"*** {pseudo} a quitté le tchat. ***"
            print(msg_depart)
            broadcast(msg_depart.encode('utf-8'))
            client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[SERVEUR] Lancé sur le port {PORT}. En attente de connexions...")

    while True:
        client_socket, addr = server.accept()
        clients.append(client_socket)
        # Un thread séparé pour chaque client connecté
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    main()

