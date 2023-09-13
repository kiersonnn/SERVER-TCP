import socket
import threading

host= '192.168.56.1'
port= 5252
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
nicknames = []
clients = []
def broadcast(message):               #sending message to all clients
    for client in clients:
        client.send(message)

def handle(client):                   #message handling from clients
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break
def receive():
    while True:
        client, address = server.accept()   #users and connections accept
        print(" Connected with '' ".format(str(address)))


        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')    #request and set nicknames
        nicknames.append(nickname)
        clients.append(client)
        print(" Nickname is {} ".format(nickname))
        broadcast(" {} joined ".format(nickname).encode('ascii'))
        client.send(' Connected to server '.encode('ascii'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
receive()




