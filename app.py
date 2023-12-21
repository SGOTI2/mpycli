import os, time, sys
import xml.etree.ElementTree as ET
CMDRUN = False
if len(sys.argv) > 1:
    CMDRUN = True
if not CMDRUN: print("Parsing...")
tree = ET.parse(os.path.dirname(__file__)+"\\struct.xml")
root = tree.getroot()
commands = []
SPECIALCOMMANDS = 3
NOT_DEFINED = -1
BATCH = 0
PYTHON = 1
POWERSHELL = 2
for i in root.findall("command"):
    currAdd = {
        'name': "",
        'type': NOT_DEFINED,
        'filepath': "",
        'localfilepath': "",
        'storage': ''
    }
    currAdd["name"] = i.find("name").text
    match i.find("type").text:
        case "batch":
            currAdd["type"] = BATCH
        case "powershell":
            currAdd["type"] = POWERSHELL
        case "python":
            currAdd["type"] = PYTHON
            try:
                currAdd["storage"] = i.find("storage").text
            except:
                pass
    currAdd["filepath"] = os.path.dirname(__file__)+i.find("path").text+i.find("filename").text
    currAdd["localfilepath"] = i.find("path").text+i.find("filename").text
    if not CMDRUN: print(currAdd)
    commands.append(currAdd)
if not CMDRUN: print("Parsing Finished")
def nwin(*args):
    if len(args[0]) >= 1:
        rcmd = args[0].pop(0)
        for i in range(len(commands)):
            if rcmd == commands[i]["name"]:
                startCmd = 'start \"\" '+execCommand(args[0], command=commands[i], run=False)
                print(startCmd)
                os.system(startCmd)
                return False
    else:
        print("Command required")
def notSpecialCommand(*args, cmd):
    match cmd:
        case "exit":
            exit()
        case "nwin":
            nwin(args[0])
        case "list":
            print(f"{'Command Name': <15} | {'File Path': <30} | {'Storage Name': <24} |")
            print(f"{'':-<15}-+-{'':-<30}-+-{'':-<24}-+")
            print(f"{'exit': <15} | {chr(92)+'app.py (built in)': <30} | {'': <24} |") # chr(92) = \
            print(f"{'nwin': <15} | {chr(92)+'app.py (built in)': <30} | {'': <24} |")
            print(f"{'list': <15} | {chr(92)+'app.py (built in)': <30} | {'': <24} |")
            for i in commands:
                print(f'{i["name"]: <15} | {i["localfilepath"]: <30} | {i["storage"]: <24} |')
        case "":
            return False
        case _:
            return True
    return False
def execCommand(*kargs, command, run=True):
    args = ' '.join(kargs[0])
    try:
        cmd = ""
        match command['type']:
            case 0: # Batch
                if run: # If running in terminal
                    cmd = f'"{command["filepath"]} {args}"'
                else: # If nwin
                    cmd = f'cmd.exe /C \"{command["filepath"]} {args}\"'
            case 1: # Python
                cmd = f'python.exe \"{command["filepath"]}\" {args}'
            case 2: # Powershell
               cmd = f'powershell.exe -executionpolicy remotesigned -File {command["filepath"]} {args}'
        if run:
            os.system(cmd)
        else:
            return cmd
    except KeyboardInterrupt:
        if not CMDRUN: print("Command Terminated")
def checkInput(inputData):
    args: list[str] = inputData.split(" ")
    commandInput = args[0]
    args.pop(0)
    if notSpecialCommand(args, cmd=commandInput):
        for i in range(len(commands)):
            if commandInput == commands[i]["name"]:
                execCommand(args,command=commands[i])
                return
        print("Command Not Found")
def inputLoopCall():
    inputed = input("> ")
    checkInput(inputed)
if not CMDRUN:
    now = time.localtime(time.time())
    buildTime = str(now.tm_mon)+str(now.tm_mday)+str(now.tm_year)+str(now.tm_hour)+str(now.tm_min)+str(now.tm_sec)
    os.system("cls")
    print("MPYCLI - Mini Python CLI")
    print(f'Version: {root.find("version").text} SDAT-{buildTime}, {len(commands)+SPECIALCOMMANDS} Commands')
    while True:
        try:
            inputLoopCall()
        except KeyboardInterrupt:
            print("\nPlease use 'exit' next time\n")
            exit()
else:
    sys.argv.pop(0)
    checkInput(' '.join(sys.argv))