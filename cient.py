import socket
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext

# --- CONFIGURATION ---
IP_SERVEUR = '127.0.0.1'  # Mets l'IP du serveur ici
PORT_SERVEUR = 50000

class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Tchat entre Potes")
        self.root.geometry("400x500")

        self.client_socket = None

        # --- Fenêtre de connexion (Pseudo) ---
        self.frame_login = tk.Frame(self.root)
        self.frame_login.pack(pady=20)

        tk.Label(self.frame_login, text="Choisis ton Pseudo :", font=("Arial", 11)).pack(pady=5)
        self.entry_pseudo = tk.Entry(self.frame_login, font=("Arial", 11))
        self.entry_pseudo.pack(pady=5)
        self.entry_pseudo.focus()

        self.btn_connect = tk.Button(self.frame_login, text="Rejoindre le Tchat", command=self.connecter)
        self.btn_connect.pack(pady=10)

        # --- Zone de Tchat (Masquée au départ) ---
        self.frame_chat = tk.Frame(self.root)

        self.area_messages = scrolledtext.ScrolledText(self.frame_chat, state='disabled', wrap='word')
        self.area_messages.pack(padx=10, pady=10, fill='both', expand=True)

        self.entry_msg = tk.Entry(self.frame_chat, font=("Arial", 11))
        self.entry_msg.pack(padx=10, pady=5, side='left', fill='x', expand=True)
        self.entry_msg.bind("<Return>", self.envoyer_message)

        self.btn_send = tk.Button(self.frame_chat, text="Envoyer", command=self.envoyer_message)
        self.btn_send.pack(padx=10, pady=5, side='right')

    def connecter(self):
        pseudo = self.entry_pseudo.get().strip()
        if not pseudo:
            messagebox.showwarning("Attention", "Mets un pseudo valide !")
            return

        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((IP_SERVEUR, PORT_SERVEUR))
            
            # Envoi du pseudo au serveur
            self.client_socket.send(pseudo.encode('utf-8'))

            # Basculer l'affichage vers le tchat
            self.frame_login.pack_forget()
            self.frame_chat.pack(fill='both', expand=True)

            # Lancer le thread pour écouter les messages entrants
            thread_receive = threading.Thread(target=self.recevoir_messages)
            thread_receive.daemon = True
            thread_receive.start()

            self.afficher_message(f"--- Connecté en tant que {pseudo} ---")

        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de se connecter au serveur.\n{e}")

    def envoyer_message(self, event=None):
        msg = self.entry_msg.get().strip()
        if msg and self.client_socket:
            try:
                self.client_socket.send(msg.encode('utf-8'))
                # Affiche son propre message directement
                self.afficher_message(f"Moi: {msg}")
                self.entry_msg.delete(0, tk.END)
            except:
                self.afficher_message("--- Erreur d'envoi ---")

    def recevoir_messages(self):
        while True:
            try:
                msg = self.client_socket.recv(1024).decode('utf-8')
                if not msg:
                    break
                self.afficher_message(msg)
            except:
                break

    def afficher_message(self, message):
        self.area_messages.config(state='normal')
        self.area_messages.insert(tk.END, message + "\n")
        self.area_messages.config(state='disabled')
        self.area_messages.yview(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatClient(root)
    root.mainloop()
