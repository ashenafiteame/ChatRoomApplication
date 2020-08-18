import socket
from threading import Thread

host = '127.0.0.1'
port = 8080

clients = {}
address = {}

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))


def broadcast(msg, prefex=""):
    for x in clients:
        x.send(bytes(prefex, "utf8") + msg)
    pass


def handle_client(conn, address):
    name = conn.recv(1024).decode()
    welcome = "Welcome " + name + ", Type #quite to leave the chat room"
    conn.send(bytes(welcome, "utf8"))
    msg = name + " has recently joined"

    broadcast(bytes(msg, "utf8"))
    clients[conn] = name

    while True:
        msg = conn.recv(1024)
        if msg != bytes('#quite', 'utf8'):
            broadcast(msg, name + ":")
        else:
            conn.send(bytes("#quite", "utf8"))
            conn.close()
            del clients[conn]
            broadcast(bytes(name + " has left "))


def accept_client_connection():
    while True:
        client_conn, client_address = sock.accept()
        print(client_address, " has connected")
        client_conn.send("welcome to the chat room".encode('utf8'))
        address[client_conn] = client_address

        Thread(target=handle_client, args=(client_conn, client_address)).start()


if __name__ == '__main__':
    sock.listen(5)
    print("the socket is running  and listening to clients")

    t1 = Thread(target=accept_client_connection)
    t1.start()
    t1.join()
