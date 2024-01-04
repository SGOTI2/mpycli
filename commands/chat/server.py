import socket
import os
import threading
import sys
# device's IP address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5001
args = []
argsStr = ' '.join(sys.argv).split("-")
argsStr.pop(0)
for i in argsStr:
    args.append(i.split(" "))
for i in args:
    match i[0]:
        case "port":
            try:
                SERVER_PORT = str(i[1])
            except IndexError:
                print("A port must be specified to use")
# receive 4096 bytes each time
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"
requestType = {
    "init": "init",
    "terminate": "kill"
}
# create the server socket
# TCP socket
s = socket.socket()
# bind the socket to our local address
s.bind((SERVER_HOST, SERVER_PORT))
# enabling our server to accept connections
# 5 here is the number of unaccepted connections that
# the system will allow before refusing new connections
s.listen(100)
print("[*] IP: "+socket.gethostbyname(socket.gethostname()))
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
callbackList = []
def callback(message):
    for i in callbackList:
        clientConnectionSend(i[0], int(i[1]), message)
# accept connection if there is any
# receive the file infos
# receive using client socket, not server socket
def clientConnectionSend(ip, port, message):
    try:
        s = socket.socket() # create socket
        s.connect((ip, port))
        s.send(f"".encode())
        for i in range(len(message) % BUFFER_SIZE):
            sending = message[i*BUFFER_SIZE:(i+1)*BUFFER_SIZE:1]
            s.sendall(sending.encode("utf-8"))
    except:
        print(f"Client Connection Send Failed to {ip}:{port}")
    s.close()
def terminateClient(ip, port, appending):
    print(f"[SYSTEM][{ip}:{port}] Terminated Connection")
    if callbackList.__contains__(appending):
        callbackList.pop(callbackList.index(appending))
    else:
        print("Failed to terminate: ", appending)
    callback(f"[SYSTEM][{ip}] Disconnected")
pastMessages = []
global client_socket
def serverInput():
    try:
        while True:
            inp = str(input(""))
            myip = socket.gethostbyname(socket.gethostname())
            callback(f"[SERVER][{myip}] {inp}")
    except:
        callback("_terminate_")
        s.close()
        client_socket.close()
        os._exit(0)
serverIn = threading.Thread(target=serverInput)
serverIn.start()
try:
    while True:
        client_socket, address = s.accept()
        # if below code is executed, that means the sender is connected
        received = client_socket.recv(BUFFER_SIZE).decode()
        ip, port, reqType, filesize = received.split(SEPARATOR)
        appending = (ip, port)
        if reqType == requestType["init"]:
            if not callbackList.__contains__(appending):
                callbackList.append(appending)
                print(f"Established New Connection: {ip}")
                callback(f"[SYSTEM][{ip}] Connected")
                client_socket.close()
                continue
        if reqType == requestType["terminate"]:
            terminateClient(ip, port, appending)
            continue
        # start receiving the file from the socket
        # and writing to the file stream
        base = "["+str(ip)+"] "
        final = base
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
        if final == base:
            print(f"[SYSTEM][{ip}:{port}] Empty Message")
            continue
        if final == base+"_terminate_":
            terminateClient(ip, port, appending)
            continue
        # close the client socket
        # close the server socket
        print(f"[{reqType.capitalize()}][{ip}:{port}]"+final.replace(base,""))
        pastMessages.append(final)
        if len(pastMessages) >= 51:
            pastMessages.pop(0)
        client_socket.close()
        callback(final)
except KeyboardInterrupt:
    print(f"[SYSTEM] Terminating All Connections")
    callback("_terminate_")
    s.close()
    client_socket.close()
    print(f"[SYSTEM] Server Terminated")
    exit(0)