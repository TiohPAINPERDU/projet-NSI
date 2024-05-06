import tkinter as tk
from threading import Thread
from socket import socket
import json


def receive_data():
    while True:
        data = client.recv(10000).decode()
        print(data)

        if "MSG:" in data:
            message = data[len("MSG:"):]
            chat_box.insert(tk.END, "Server: " + message + '\n')
        else:
            pos = json.loads(data)
            start_x, start_y, end_x, end_y = pos["start_x"], pos["start_y"], pos["end_x"], pos["end_y"]
            print(type(canvas))
            
            canvas.create_line(start_x, start_y, end_x, end_y,width=5)
            print("hello")

def draw_line(start_x, start_y, end_x, end_y):
    canvas.create_oval(start_x, start_y, end_x, end_y)
    print("heey")

def send_message(event=None):
    message = user_input.get()
    if message:
        chat_box.insert(tk.END, "You: " + message + '\n')
        client.send(message.encode())
        user_input.delete(0, tk.END)

client = socket()
client.connect(('192.168.0.179', 25562))
print("bien connecté")
#-------------------------------------------------------------------------------

app = tk.Tk()
app.title("Chat App")

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

#--------------------------------------------------------------------------------

receive_thread = Thread(target=receive_data)
receive_thread.start()

app.mainloop()
