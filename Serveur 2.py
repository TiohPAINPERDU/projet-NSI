import tkinter as tk
from threading import Thread
from socket import socket
import random
import time 
import json

liste_mots = ["chat", "chien", "oiseau", "poipi", "voiture", "arbre"]
end_x, end_y = 0 ,0
p = 0
mot = random.choice(liste_mots)

start = time.time()

def receive_messages():
    while True:
        message = client.recv(1000)
        if message:
            chat_box.insert(tk.END, message.decode() + '\n')
            if message.decode() == mot:
                client.send(("MSG:GAGNéééé").encode())
                
def send_message(event=None):
    message = user_input.get()
    if message:
        chat_box.insert(tk.END, "You: " + message + '\n')
        client.send(("MSG:" + message).encode())
        user_input.delete(0, tk.END)    

def draw(start_x,start_y):
    global end_x, end_y 
    canvas.create_line(start_x, start_y, end_x, end_y)
    end_x, end_y = start_x, start_y
    send_positions(start_x,start_y,end_x,end_y)

def send_positions(start_x, start_y, end_x, end_y):
    time.sleep(1)
    pos = {"start_x": start_x, "start_y": start_y, "end_x": end_x, "end_y": end_y}
    client.send(json.dumps(pos).encode())


def pos1(event):
    global start_x, start_y, p
    start_x = event.x
    start_y = event.y
    print(start_x,start_y)
    if p == 1:
        global end_x, end_y
        end_x = start_x + 1
        end_y = start_y + 1
        p = p-1
    print(p)
    draw(start_x, start_y)
    app.after(300, pos1)

#def pos2(event):
 #   global p
  #  p = 1
   # print(p)
def pos2(event):
    global end_x, end_y
    end_x = event.x
    end_y = event.y
    print(end_x, end_y)
    draw(start_x, start_y, end_x, end_y)


serveur = socket()
serveur.bind(('192.168.0.179', 25562))
serveur.listen()
client, ip = serveur.accept()
print("conexion du client à", ip, "ipv4")

#------------------------------------------------------------------------------------------

app = tk.Tk()
app.title("serv")

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
canvas.bind("<B1-Motion>", pos1)
canvas.bind("<ButtonRelease-1>", pos2)

#------------------------------------------------------------------------------------------------

receive_thread = Thread(target=receive_messages)
send_thread = Thread(target=send_message)
receive_thread.start()
send_thread.start()


app.mainloop()
