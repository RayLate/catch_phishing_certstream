import socket, threading

lock = threading.Lock()
queue = []
dict = {'1'}

class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        print("New connection added: ", clientAddress)

    def run(self):
        print("Connection from : ", clientAddress)
        # self.csocket.send(bytes("Hi, This is from Server..",'utf-8'))
        msg = ''
        while True:
            data = self.csocket.recv(2048)
            msg = data.decode()

            global lock
            global queue
            global dict
            lock.acquire()
            if msg == '1':
                to_send = None
                if len(queue) != 0:
                    print(len(queue))
                    to_send = queue.pop(-1)
                else:
                    to_send = '1'
                lock.release()
                to_send = to_send.encode('utf-8')
                self.csocket.send(to_send)

            else:
                if msg in dict:
                    lock.release()
                else:
                    dict.add(msg)
                    queue.append(msg)
                    lock.release()


        print("Client at ", clientAddress, " disconnected...")


LOCALHOST = "172.26.191.206"
PORT = 8080
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print("Server started")
print("Waiting for client request..")

while True:
    server.listen(5)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock)
    newthread.start()