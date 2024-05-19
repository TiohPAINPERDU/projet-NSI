import tkinter as tk
from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM
import random
import json

limit = 10
time_left = 60 

liste_mots = ["chat", "chien", "oiseau", "poipi", "voiture", "arbre"]
mot = random.choice(liste_mots)
liste_co = []

 #-------------------------------------------ici---------------------------------------------------
def setup_server():
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(('192.168.0.179', 25562))
    server_socket.listen()
    client_socket, ip_address = server_socket.accept()
    print("Client connected from:", ip_address)
    return client_socket
client = setup_server()
#---------------------------------------------------------------------------------------------------
def receive_messages():
    while True:
        try:
            message = client.recv(1000).decode()
            if message:
                if "MSG:" in message:
                    chat_box.insert(tk.END, message[4:] + '\n')
                    if message[4:] == mot:
                        client.send("MSG:GAGNéééé".encode())
                        app.after(30,stop())
                else:
                    pos = json.loads(message)
                    start_x, start_y, end_x, end_y = pos["start_x"], pos["start_y"], pos["end_x"], pos["end_y"]
                    canvas.create_line(start_x, start_y, end_x, end_y)
                    liste_co.append((start_x, start_y, end_x, end_y))
        except Exception as e:
            print(f"Error receiving data: {e}")
            break

def send_message(event=None):
    message = user_input.get()
    if message:
        chat_box.insert(tk.END, "You: " + message + '\n')
        client.send(("MSG:" + message).encode())
        user_input.delete(0, tk.END)

def start_drawing(event):
    global start_x, start_y
    start_x, start_y = event.x, event.y

def draw(event):
    global start_x, start_y, end_x, end_y
    end_x, end_y = event.x, event.y
    canvas.create_line(start_x, start_y, end_x, end_y,width=5)
    pos = {"start_x": start_x, "start_y": start_y, "end_x": end_x, "end_y": end_y}
    client.send(json.dumps(pos).encode())
    start_x, start_y = end_x, end_y



def update_timer():
    global time_left
    if time_left > 0:
        time_left -= 1
        TimerL.config(text=f"Time left: {time_left}s")
        app.after(1000, update_timer)       
    elif time_left == 0:
        chat_box.insert(tk.END, "Perduuuuu" + '\n') 
        app.after(300, stop())   

def stop():
    app.quit()


#--------------------------------------------------------------------------------
app = tk.Tk()
app.title("Server")

mot_label = tk.Label(app, text=f"Mot choisi: {mot}")
mot_label.pack()

TimerL = tk.Label(app, text=f"Time left: {time_left}s")
TimerL.pack()

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
user_input.bind("<Return>", send_message)

send_button = tk.Button(input_frame, text="Send", command=send_message)
send_button.pack(side=tk.LEFT)

canvas = tk.Canvas(app, width=1000, height=1000, bg="white")
canvas.pack()


canvas.bind("<ButtonPress-1>", start_drawing)  
canvas.bind("<B1-Motion>", draw)  
#----------------------------------------------------------------------------------------------

receive_thread = Thread(target=receive_messages, daemon=True)
receive_thread.start()

update_timer()

app.mainloop()
