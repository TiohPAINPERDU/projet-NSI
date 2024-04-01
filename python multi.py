import tkinter as tk
from threading import Thread
from socket import socket
import random

# Liste des mots disponibles
liste_mots = ["chat", "chien", "oiseau", "maison", "voiture", "arbre"]

# Choix aléatoire d'un mot parmi la liste
mot = random.choice(liste_mots)

def receive_messages():
    while True:
        message = sclient.recv(1000)
        if message:
            chat_box.insert(tk.END, message.decode() + '\n')
            if message.decode() == mot:
                sclient.send(("MSG:GANGé").encode())
def send_message(event=None):
    message = user_input.get()
    if message:
        chat_box.insert(tk.END, "You: " + message + '\n')
        sclient.send(("MSG:" + message).encode())
        user_input.delete(0, tk.END)    

def draw(event):
    x, y = event.x, event.y
    colored_pixels.append((x, y))
    canvas.create_rectangle(x, y, x+5, y+5, fill="black")
    half = len(colored_pixels)//2
    del colored_pixels[:half]
    send_positions(colored_pixels)

def send_positions(positions):
    position_str = f"POS: {positions[0][0]}, {positions[0][1]}"
    sclient.send(position_str.encode())

serveur = socket()
serveur.bind(('192.168.0.179', 25562))
serveur.listen()
(sclient, adclient) = serveur.accept()

app = tk.Tk()
app.title("serv")

# Affichage du mot choisi au hasard
mot_label = tk.Label(app, text=f"Mot choisi: {mot}")
mot_label.pack()

chat_frame = tk.Frame(app)
chat_frame.pack(padx=30, pady=30)

chat_box = tk.Text(chat_frame, height=20, width=50)
chat_box.pack(side=tk.LEFT)

scrollbar = tk.Scrollbar(chat_frame, command=chat_box.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
chat_box.config(yscrollcommand=scrollbar.set)

input_frame = tk.Frame(app)
input_frame.pack(padx=10, pady=10)

user_input = tk.Entry(input_frame, width=50)
user_input.pack(side=tk.LEFT)

send_button = tk.Button(input_frame, text="Send", command=send_message)
send_button.pack(side=tk.LEFT)

canvas = tk.Canvas(app, width=1000, height=1000, bg="white")
canvas.pack()
canvas.bind("<B1-Motion>", draw)

colored_pixels = []

receive_thread = Thread(target=receive_messages)
receive_thread.start()

app.mainloop()
