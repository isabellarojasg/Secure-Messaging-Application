import socket
import threading

user_name = input("Username: ")
user_password = input("Password: ")
chat_history = {}
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9090))

#This function should accept the clients credentials and print the messages
def verify():
    while True:
        try:
            
            message = client.recv(1024).decode('ascii')
            if message == 'USER':
                client.send(user_name.encode('ascii'))
            elif message == 'PASS':
                client.send(user_password.encode('ascii'))
            else:
                print(message)
        except:
            print("An error occurred!")
            client.close()

#This function allows cliwnts to write their messages out to other connected clients
def write():
    while True:
        msg = f'{user_name}:{input("")}'
        client.send(msg.encode('ascii'))

receive_thread = threading.Thread(target=verify)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
