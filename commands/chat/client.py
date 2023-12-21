import socket
import threading
import os
import sys
host = ""
# the port, let's use 5001
port = 5001
args = []
INPUT_PORT = 5002
INPUT_HOST = "0.0.0.0"
argsStr = ' '.join(sys.argv).split("-")
argsStr.pop(0)
for i in argsStr:
    args.append(i.split(" "))
for i in args:
    match i[0]:
        case "ip":
            try:
                host = str(i[1])
            except IndexError:
                print("A ip address must be specified to use")
        case "port":
            try:
                port = int(i[1])
            except IndexError:
                print("A port must be specified to use")
        case "inport":
            try:
                INPUT_PORT = int(i[1])
            except IndexError:
                print("A port must be specified to use")

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 
# the ip address or hostname of the server, the receiver
if host == "":
    host = input("IP>")
def initialRequest():
    s = socket.socket() # create socket
    s.connect((host, port))
    myip = socket.gethostbyname(socket.gethostname())
    s.send(f"{myip}{SEPARATOR}{INPUT_PORT}{SEPARATOR}".encode())
    s.close()
    print(f"[LOCAL_SYSTEM] Connection Established to {host}:{port}")
def killConnection():
    global sin
    s = socket.socket() # create socket
    s.connect((host, port))
    myip = socket.gethostbyname(socket.gethostname())
    s.send(f"{myip}{SEPARATOR}{INPUT_PORT}{SEPARATOR}".encode())
    s.sendall('_terminate_'.encode("utf-8"))
    s.close()
    sin.close()
    print(f"[LOCAL_SYSTEM] Terminated Connection to {host}:{port}")
initialRequest()
global sin
sin = socket.socket()
sin.bind((INPUT_HOST, INPUT_PORT))
# enabling our server to accept connections
# 5 here is the number of unaccepted connections that
# the system will allow before refusing new connections
sin.listen(5)
def inConnect():
    global sin
    try:
        while True:
            client_socket, address = sin.accept() 
            # if below code is executed, that means the sender is connected
            # start receiving the file from the socket
            # and writing to the file stream
            final = ""
            while True:
                # read 1024 bytes from the socket (receive)
                bytes_read = client_socket.recv(BUFFER_SIZE)
                if not bytes_read:    
                    # nothing is received
                    # file transmitting is done
                    break
                # write to the file the bytes we just received
                final+=str(bytes_read, encoding="utf-8")
                # update the progress bar
            if final == "_terminate_":
                sin.close()
                client_socket.close()
                print("[SYSTEM] Server Terminated Connection")
                os._exit(0)
            # close the client socket
            # close the server socket
            myip = socket.gethostbyname(socket.gethostname())
            final = final.replace("[SERVER]["+host+"]", "[\x1b[1;31mSERVER\x1B[0m][\x1b[1;31m"+host+"\x1B[0m]")
            final = final.replace("["+myip+"]", "[\x1b[1;32m"+myip+"\x1B[0m]")
            print(final)
    except KeyboardInterrupt:
        return
    except:
        os._exit(0)
inThread = threading.Thread(target=inConnect)
inThread.start()
try:
    while True:
        message = str(input(""))
        s = socket.socket() # create socket
        s.connect((host, port))
        myip = socket.gethostbyname(socket.gethostname())
        s.send(f"{myip}{SEPARATOR}{INPUT_PORT}{SEPARATOR}".encode())
        for i in range(len(message) % BUFFER_SIZE):
            sending = message[i*BUFFER_SIZE:(i+1)*BUFFER_SIZE:1]
            s.sendall(sending.encode("utf-8"))
        s.close()
except KeyboardInterrupt:
    killConnection()
    os._exit(0)