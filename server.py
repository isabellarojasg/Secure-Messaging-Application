#!/usr/bin/python3
import socket
import threading
import os

host = '127.0.0.1'
port = 9090


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))

server.listen()

clients = []
#to manage clients
user_names = []

user_passwords = []

#We want to have many diferent threads beacuse we want to have
# many processes running at the same time

# This function sends one message to all the connected clients
# input: an already encoded message
def broadcast(message):
    for client in clients:
        client.send(message)

#handle individual connections
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            user_name = user_names[index]
            broadcast(f'{user_name} left the chat!'.encode('ascii'))
            user_names.remove(user_name)
            break

# Listen and accept new clients connections
def recieve():
    while True:

        #accept returns client and address
        client, address = server.accept()
        print(f"Connected with {str(address)}!")

        #we should use the key here
        client.send("USER".encode('ascii'))
        user_name = client.recv(1024).decode('ascii')

        client.send("PASS".encode('ascii'))
        user_password = client.recv(1024).decode('ascii')

        user_names.append(user_name)
        user_passwords.append(user_password)
        clients.append(client)

        print(f"Username of the client is {user_name}")
        broadcast(f"{user_name} joined the chat!\n".encode('ascii'))
        client.send("Connected to the server".encode('ascii'))

        #for each client we are going to have a different thread
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server running...")
os.system('python init_database.py')
print("complete initial server database")
recieve()
