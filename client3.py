import tkinter as tk
from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM
import json
import time

limit = 10
time_left = 60

#----------------------------------------------------------------------------------------------

client = socket(AF_INET, SOCK_STREAM)
client.connect(('192.168.0.179', 25562))
print("Connected to server")

#----------------------------------------------------------------------------------------------

def receive_data():
    while True:
        try:
            data = client.recv(10000).decode()
            if data:
                if data.startswith("MSG:"):
                    message = data[4:]
                    chat_box.insert(tk.END, "Other: " + message + '\n')
                    if message == "Gagné":
                        app.after(300, stop)
                else:
                    pos = json.loads(data)
                    start_x, start_y, end_x, end_y = pos["start_x"], pos["start_y"], pos["end_x"], pos["end_y"]
                    canvas.create_line(start_x, start_y, end_x, end_y, width=5)
        except Exception as e:
            print(f"Error receiving data: {e}")
            break

def send_message(event=None):
    message = user_input.get()
    if message:
        chat_box.insert(tk.END, "You: " + message + '\n')
        client.send(("MSG:" + message).encode())
        user_input.delete(0, tk.END)

def update_timer():
    global time_left
    if time_left > 0:
        time_left -= 1
        TimerL.config(text=f"Time left: {time_left}s")
        app.after(1000, update_timer)
    elif time_left == 0:
        chat_box.insert(tk.END, "Perduuuuu" + '\n')
        app.after(500, stop)

def stop():
    time.sleep(2)
    app.quit()

#----------------------------------------------------------------------------------------------

app = tk.Tk()
app.title("Client")

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

#----------------------------------------------------------------------------------------------

receive_thread = Thread(target=receive_data, daemon=True)
receive_thread.start()

update_timer()
app.mainloop()
