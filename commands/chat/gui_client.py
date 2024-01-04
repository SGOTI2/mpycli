








# You have to run the file, right click this file and click 'open with', select python
# Remember you have to have python installed









import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import socket
import threading
from sys import argv
## Updater ###########################
import typing
import urllib.error
import urllib.parse
import urllib.request
from email.message import Message
from os import path, replace
class Response(typing.NamedTuple):
    body: str
    headers: Message
    status: int
    error: bool = False
def request(url: str) -> Response:
    if not url.casefold().startswith("http"):
        raise urllib.error.URLError("Incorrect and possibly insecure protocol in url")
    httprequest = urllib.request.Request(url, data=None, headers={"Accept": "text/text"}, method="GET")
    try:
        with urllib.request.urlopen(httprequest) as httpresponse:
            response = Response(headers=httpresponse.headers, status=httpresponse.status, body=httpresponse.read().decode(httpresponse.headers.get_content_charset("utf-8")),)
    except urllib.error.HTTPError as e:
        response = Response(body=str(e.reason),headers=e.headers,status=e.code,error=True)
    except urllib.error.URLError as e:
        response = Response(body=str(e.reason),headers={},status=500,error=True)
    return response
def CheckForUpdate():
    verReq = request("https://raw.githubusercontent.com/SGOTI2/mpycli/main/commands/chat/version.txt")
    if verReq.status != 200:
        return ('',[])
        pass
    myVer = "0"
    with open(path.join(path.abspath(path.dirname(__file__)),"version.txt"),"r") as f:
        myVer = f.read()
    if verReq.body != myVer:
        return (myVer.split(",")[0], verReq.body.split(","))
    else:
        return ('',[])
def DownloadUpdate(_, updateInfo):
    if updateInfo == ('',[]):
        print("Update is empty!")
        return
    print(f"Downloading Update, version {updateInfo[0]}")
    installPath = path.abspath(path.dirname(__file__))
    print(f"Installing to: {installPath}")
    fileNum = 0
    updateInfo.pop(0)
    updateInfo.pop(0)
    installInfo = []
    for i in updateInfo:
        print(f"Downloading {i} [{fileNum}/{len(updateInfo)}]")
        fileNum += 1;
        fileRequest = request(f"https://raw.githubusercontent.com/SGOTI2/mpycli/main/commands/chat/{i}")
        print(f"Request received, status: {fileRequest.status}")
        if fileRequest.error:
            print(f"[ERROR] Request has a Error. File not downloaded, please try again to update this file.")
            continue
        writingLocation = path.join(installPath, i.split("\n")[0]+".updatepart")
        print(f"Writing File: {writingLocation}")
        with open(writingLocation, "wb") as f:
            f.write(fileRequest.body.encode("utf-8"))
        print(f"Writing complete for file")
        installInfo.append(writingLocation)
    print("Download Complete, ready to install")
    installUpdate(installInfo)
def installUpdate(installInfo):
    for i in installInfo:
        newList = i.split(".")
        newList.pop(len(newList)-1)
        new = '.'.join(newList)
        print(f"{i}=>{new}")
        replace(i, new)
## End Updater ###########################
class ConnectionHandler():
    def __init__(self, host: str, port: int, inIP: str, inPort: int):
        self.SEPARATOR = "<SEPARATOR>"
        self.BUFFER_SIZE = 4096
        self.host = host
        self.port = port
        self.inIP = inIP
        self.inPort = inPort
        self.connected = False
    def getMyIP(self):
        return socket.gethostbyname(socket.gethostname())
    def initialConnection(self):
        s = socket.socket()
        s.connect((self.host, self.port))
        s.send(f"{self.getMyIP()}{self.SEPARATOR}{self.inPort}{self.SEPARATOR}init{self.SEPARATOR}".encode())
        s.close()
        print(f"Connection Established to {self.host}:{self.port}")
        self.connected = True
    def terminate(self):
        if self.connected:
            if "sin" in dir(self):
                self.sin.close()
            s = socket.socket()
            s.connect((self.host, self.port))
            s.send(f"{self.getMyIP()}{self.SEPARATOR}{self.inPort}{self.SEPARATOR}kill{self.SEPARATOR}".encode())
            s.sendall('_terminate_'.encode("utf-8"))
            s.close()
            print(f"Terminated Connection to {self.host}:{self.port}")
        else:
            print("You have already disconnected")
        self.connected = False
    def ThreadFReceiving(self, callback):
        try:
            while True:
                client_socket, address = self.sin.accept() 
                final = ""
                while True:
                    bytes_read = client_socket.recv(self.BUFFER_SIZE)
                    if not bytes_read:    
                        break
                    final+=str(bytes_read, encoding="utf-8")
                if final == "_terminate_":
                    self.sin.close()
                    del self.sin
                    client_socket.close()
                    self.terminate()
                    print("[SYSTEM] Server Terminated Connection")
                    return
                try:
                    callback(final)
                except:
                    print("Error occurred in callback")
        except KeyboardInterrupt:
            return
        except Exception as e:
            print(e)
    def startReceiving(self, callback):
        self.sin = None
        self.sin = socket.socket()
        self.sin.bind((self.inIP, self.inPort))
        self.sin.listen(5)
        self.receivingThread = threading.Thread(target=self.ThreadFReceiving, args={callback}, daemon=True)
        self.receivingThread.start()
    def send(self, message):
        s = socket.socket()
        s.connect((self.host, self.port))
        s.send(f"{self.getMyIP()}{self.SEPARATOR}{self.inPort}{self.SEPARATOR}message{self.SEPARATOR}".encode())
        for i in range(len(message) % self.BUFFER_SIZE):
            sending = message[i*self.BUFFER_SIZE:(i+1)*self.BUFFER_SIZE:1]
            s.sendall(sending.encode("utf-8"))
        s.close()



class App(tk.Tk):
    def ThreadFCheckUpdate(self):
        updateCheck = CheckForUpdate()
        if updateCheck != ('',[]):
            if updateCheck[1][1] == "r":
                self.title("")
                self.lockout = True
                responce = messagebox.askokcancel("MPYCLI - Chat - Outdated Client!", f"Your client version is outdated.\nYou MUST download the update, would you like to do so?\n\n{updateCheck[0]}=>{updateCheck[1][0]}")
                if responce == True:
                    self.ThreadUpdate = threading.Thread(target=DownloadUpdate, args=(updateCheck))
                    self.ThreadUpdate.start()
                    self.ThreadUpdate.join()
                self.FClose()
            else:
                responce = messagebox.askquestion("MPYCLI - Chat - Outdated Client!", f"Your client version is outdated.\n\nWould you like to download the update?\n\n{updateCheck[0]}=>{updateCheck[1][0]}")
            if responce == 'yes':
                self.ThreadUpdate = threading.Thread(target=DownloadUpdate, args=(updateCheck))
                self.ThreadUpdate.start()
                self.ThreadUpdate.join()
                self.FClose()
    def __init__(self, startArgs):
        super().__init__()
        self.ThreadUpdateCheck = threading.Thread(target=self.ThreadFCheckUpdate, daemon=True)
        self.ThreadUpdateCheck.start()
        #self.FDarkMode()
        self.root = ttk.Frame(self)#, style="Dark.TFrame")
        self.FLoadSetup(startArgs)
        self.root.pack(fill=tk.BOTH, expand=True)
        self.protocol("WM_DELETE_WINDOW", self.FClose)
    def FClose(self):
        if "connectionHandler" in dir(self):
            self.connectionHandler.terminate()
        self.destroy()
    def FErrorThrow(self, message):
        messagebox.showerror("MPYCLI - Chat - Error!", message)
    def FDarkMode(self):
        dark_theme = {
            ".": { 
                "configure": {
                    "background": "#2d2d2d",  # Dark grey background
                    "foreground": "white",    # White text
                }
            },
            "TListBox": { 
                "configure": {
                    "background": "#2d2d2d",  # Dark grey background
                    "foreground": "white",    # White text
                }
            },
            "TLabel": {
                "configure": {
                    "foreground": "white",    # White text
                }
            },
            "TButton": {
                "configure": {
                    "background": "#3c3f41",  # Dark blue-grey button
                    "foreground": "white",    # White text
                }
            },
            "TEntry": {
                "configure": {
                    "background": "#2d2d2d",  # Dark grey background
                    "foreground": "white",    # White text
                    "fieldbackground" : "#4d4d4d",
                    "insertcolor": "white",
                    "bordercolor" : "black",
                    "lightcolor" : "#4d4d4d",
                    "darkcolor" : "black",
                }
            },
            "TCheckbutton": {
                "configure": {
                    "foreground": "white",    # White text
                    "indicatorbackground" : "#2d2d2d", 
                    "indicatorforeground" : "white",
                }
            },
            "TCombobox": {
                "configure": {
                    "background": "#2d2d2d",  # Dark grey background
                    "foreground": "white",    # White text
                    "fieldbackground" : "#4d4d4d",
                    "insertcolor": "white",
                    "bordercolor" : "black",
                    "lightcolor" : "#4d4d4d",
                    "darkcolor" : "black",
                    "arrowcolor" : "white"
                },
            },
        }
        style = ttk.Style()
        style.theme_create('dark', parent="clam", settings=dark_theme)
        style.theme_use('dark')
    def FLoadSetup(self, startArgs):
        self.title('MPYCLI - Chat - Setup')
        self.geometry('250x230')
        self.Setup_WMain = ttk.Frame(self.root)
        # Title
        self.Setup_WTitle = ttk.Label(self.Setup_WMain, text='Chat', font=('Helvetica bold', 20))
        self.Setup_WTitle.grid(column=0, row=0, pady=10, padx=0, sticky="NSW")

        self.VUseDefault = tk.IntVar()
        # Use Defaults Button
        self.Setup_WDefault = ttk.Checkbutton(self.Setup_WMain, variable=self.VUseDefault, onvalue=1, offvalue=0, text="Default Settings", command=self.FUseDefault)
        self.Setup_WDefault.grid(column=1, row=0, sticky="NES", pady=20)

        # Get Server IP
        self.Setup_WIpLabel = ttk.Label(self.Setup_WMain, text='Server IP: ')
        self.Setup_WIpLabel.grid(column=0, row=1, sticky='E')
        # Server IP input
        self.Setup_WIp = ttk.Entry(self.Setup_WMain)
        self.Setup_WIp.grid(column=1, row=1)
        self.Setup_WIp.focus_set()

        # Get Server Port
        self.Setup_WPortLabel = ttk.Label(self.Setup_WMain, text='Server Port: ')
        self.Setup_WPortLabel.grid(column=0, row=2, sticky='E')
        # Server Port input
        self.Setup_WPort = ttk.Entry(self.Setup_WMain)
        self.Setup_WPort.grid(column=1, row=2)



        # Divider
        self.Setup_WStartDivider = ttk.Separator(self.Setup_WMain, orient="horizontal")
        self.Setup_WStartDivider.grid(column=0, row=3, pady=10, sticky='NESW', columnspan=2)




        # Get My Input IP
        self.Setup_WMyIpLabel = ttk.Label(self.Setup_WMain, text='Receiving IP: ')
        self.Setup_WMyIpLabel.grid(column=0, row=4, sticky='E')
        # My input IP input
        self.Setup_WMyIp = ttk.Entry(self.Setup_WMain)
        self.Setup_WMyIp.grid(column=1, row=4)

        # Get My input Port
        self.Setup_WMyPortLabel = ttk.Label(self.Setup_WMain, text='Receiving Port: ')
        self.Setup_WMyPortLabel.grid(column=0, row=5, sticky='E')
        # My input Port input
        self.Setup_WMyPort = ttk.Entry(self.Setup_WMain)
        self.Setup_WMyPort.grid(column=1, row=5)


        # Divider
        self.Setup_WStartBTNDivider = ttk.Separator(self.Setup_WMain, orient="horizontal")
        self.Setup_WStartBTNDivider.grid(column=0, row=6, pady=10, sticky='NESW', columnspan=2)



        # Connect Button
        self.Setup_WConnect = ttk.Button(self.Setup_WMain, text="Connect", command=self.FConnect)
        self.Setup_WConnect.grid(column=0, row=7, columnspan=2)

        self.Setup_WMain.pack()
        if startArgs != ["", 0, 0]:
            self.FDisableUseDefault()
            if startArgs[0] != "":
                self.Setup_WIP.delete(0, tk.END)
                self.Setup_WIp.insert(0, startArgs[0])
            if startArgs[1] != 0:
                self.Setup_WPort.delete(0, tk.END)
                self.Setup_WPort.insert(0, startArgs[1])
            if startArgs[2] != 0:
                self.Setup_WMyPort.delete(0, tk.END)
                self.Setup_WMyPort.insert(0, startArgs[2])
        else:
            self.FEnableUseDefault()
    def FDeconstructSetup(self):
        self.Setup_WMain.destroy()
    def FEnableUseDefault(self):
        self.VUseDefault.set(1)
        self.Setup_WPort.delete(0, tk.END)
        self.Setup_WPort.insert(0, "5001")
        self.Setup_WPort.config(state="disabled")

        self.Setup_WMyIp.delete(0, tk.END)
        self.Setup_WMyIp.insert(0, "0.0.0.0")
        self.Setup_WMyIp.config(state="disabled")

        self.Setup_WMyPort.delete(0, tk.END)
        self.Setup_WMyPort.insert(0, "5002")
        self.Setup_WMyPort.config(state="disabled")
    def FDisableUseDefault(self):
        self.VUseDefault.set(0)
        self.Setup_WPort.config(state="enabled")
        self.Setup_WMyIp.config(state="enabled")
        self.Setup_WMyPort.config(state="enabled")
    def FUseDefault(self):
        if self.VUseDefault.get() == 1:
            self.FEnableUseDefault()
        else:
            self.FDisableUseDefault()
    


    def FConnect(self):
        if 'lockout' in dir(self):
            self.FErrorThrow("You must update to connect to a server")
            return
        self.ServerIP = self.Setup_WIp.get()
        self.ServerPort = int(self.Setup_WPort.get())
        self.InputIP = self.Setup_WMyIp.get()
        if self.InputIP != "0.0.0.0":
            print("Receiving IP address is not 0.0.0.0! This will cause only your requests to be accepted!")
        self.InputPort = int(self.Setup_WMyPort.get())
        print(f"Connecting to {self.ServerIP}:{self.ServerPort}, and receiving at {self.InputIP}:{self.InputPort}")
        self.FDeconstructSetup()
        self.title('MPYCLI - Chat - Connecting')
        self.geometry('220x120')
        self.Connect_WMain = ttk.Frame(self.root)

        # Connect Title
        self.Connect_WTitle = ttk.Label(self.Connect_WMain, text="Connecting...", font=('Helvetica bold', 18))
        self.Connect_WTitle.grid(row=0, column=0, sticky="NSW")
        
        # Connect Description
        self.Connect_WDesc = ttk.Label(self.Connect_WMain, text=f"Connecting to: {self.ServerIP}:{self.ServerPort}\nReceiving at {self.InputIP}:{self.InputPort}")
        self.Connect_WDesc.grid(row=1, column=0, sticky="NSW")

        self.Connect_WMain.pack(padx=20, pady=20)
        

        # Connection Request
        self.ThreadConnect = threading.Thread(target=self.ThreadFConnect, daemon=True)
        self.ThreadConnect.start()
    def FDeconstructConnect(self):
        self.Connect_WMain.destroy()
    def ThreadFConnect(self):
        self.connectionHandler = ConnectionHandler(self.ServerIP, self.ServerPort, self.InputIP, self.InputPort)
        ranWithErrors = True
        try:
            self.connectionHandler.startReceiving(self.FGetMessage)
            self.connectionHandler.initialConnection()
            ranWithErrors = False
        except ConnectionResetError as err:
            self.FErrorThrow("Connection Reset.\nraw: "+err.strerror)
        except ConnectionRefusedError as err:
            self.FErrorThrow("Connection Refused.\nAre you sure that the server is running and the IP and port are correct?\nraw: "+err.strerror)
        except ConnectionAbortedError as err:
            self.FErrorThrow("Connection Aborted.\nA proxy or firewall may be blocking the connection.\nraw: "+err.strerror)
        except OSError as err:
            self.FErrorThrow(err.strerror)
        if ranWithErrors:
            self.FDeconstructConnect()
            self.FLoadSetup()
        print("Connected!")
        self.FChatSetup()
    def FDisconnect(self):
        self.connectionHandler.terminate()



    def FDeconstructChat(self):
        self.Chat_WMain.destroy()
    def FDisconnectButton(self):
        self.FDeconstructChat()
        self.FLoadSetup()
        self.FDisconnect()
    def FSendMessage(self, *_):
        self.connectionHandler.send(self.Chat_WInputBox.get())
        self.Chat_WInputBox.delete(0, tk.END)
    def FGetMessage(self, message):
        if "Chat_WMessages" in dir(self):
            self.Chat_WMessages.insert(tk.END, message)
    def FChatSetup(self):
        if not self.connectionHandler.connected:
            print("Your not connected!")
            return
        self.FDeconstructConnect()
        self.title(f"MPYCLI - Chat - {self.ServerIP}")
        self.geometry('400x500')
        self.Chat_WMain = ttk.Frame(self.root)

        # Header
        self.Chat_WHeader = ttk.Frame(self.Chat_WMain)

        # Disconnect Button
        self.Chat_WDisconnect = ttk.Button(self.Chat_WHeader, text="Disconnect", command=self.FDisconnectButton)
        self.Chat_WDisconnect.grid(row=0, column=0, sticky="NSW")

        # Server Info
        self.Chat_WServerInfo = ttk.Label(self.Chat_WHeader, text=f"{self.ServerIP}", font=('Helvetica bold', 12))
        self.Chat_WServerInfo.grid(row=0, column=1, sticky="NW")
        
        self.Chat_WHeader.grid(row=0, column=0, sticky="NW")
        
        
        # Chat Messages
        self.Chat_WMessageScrollbar = tk.Scrollbar(self.Chat_WMain, orient=tk.VERTICAL) 
        self.Chat_WMessages = tk.Listbox(self.Chat_WMain, yscrollcommand=self.Chat_WMessageScrollbar.set) 
        self.Chat_WMessageScrollbar.config(command=self.Chat_WMessages.yview) 

        self.Chat_WMessages.insert(0,"Connected")
        self.Chat_WMessages.grid(row=1, column=0, sticky="NEWS") 
        self.Chat_WMessageScrollbar.grid(row=1, column=1, sticky="NS")


        
        
        # Input Area
        self.Chat_WInput = ttk.Frame(self.Chat_WMain)

        # Input Box
        self.Chat_WInputBox = ttk.Entry(self.Chat_WInput)
        self.Chat_WInputBox.grid(row=0, column=0)
        self.Chat_WInputBox.bind('<Return>', self.FSendMessage)
        # Input Button
        self.Chat_WInputButton = ttk.Button(self.Chat_WInput, text="Send", command=self.FSendMessage)
        self.Chat_WInputButton.grid(row=0, column=1)
        
        self.Chat_WInput.columnconfigure(0, weight=1)
        self.Chat_WInput.grid(row=2, column=0)

        self.Chat_WMain.rowconfigure(1, weight=1)
        self.Chat_WMain.columnconfigure(0, weight=1)
        self.Chat_WMain.pack(fill=tk.BOTH, expand=True)
if __name__ == "__main__":
    startArgs = ["", 0, 0]
    args = []
    argsStr = ' '.join(argv).split("-")
    argsStr.pop(0)
    for i in argsStr:
        args.append(i.split(" "))
    for i in args:
        match i[0]:
            case "ip":
                try:
                    startArgs[0] = str(i[1])
                except IndexError:
                    print("A ip address must be specified to use")
            case "port":
                try:
                    startArgs[1] = int(i[1])
                except IndexError:
                    print("A port must be specified to use")
            case "inport":
                try:
                    startArgs[2] = int(i[1])
                except IndexError:
                    print("A port must be specified to use")
    app = App(startArgs)
    app.mainloop()