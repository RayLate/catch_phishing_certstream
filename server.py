import socket, threading
import os
from subprocess import Popen, PIPE
import signal

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


LOCALHOST = "localhost"
PORT = 8889
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    server.bind((LOCALHOST, PORT))
except OSError:
    process = Popen(["lsof", "-i", ":{0}".format(PORT)], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    for process in str(stdout.decode("utf-8")).split("\n")[1:]:
        data = [x for x in process.split(" ") if x != '']
        if (len(data) <= 1):
            continue
        os.kill(int(data[1]), signal.SIGKILL)

print("Server started")
print("Waiting for client request..")

while True:
    server.listen(5)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock)
    newthread.start()