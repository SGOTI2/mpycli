import helpers.h_store as store
import sys, os
sys.argv.pop(0)
# Open Storage File
global osf
osf = ""
def phraseCommand(command):
    global osf
    args = command.split(" ")
    cmd = args[0]
    args.pop(0)
    match cmd:
        case "exit":
            exit(0)
        case "help":
            print(
"""Storage Control

use: Open a store file and use it for modifications
    *Any*: File name or file id
delete: Delete a storage file
    *Any*: File name or file id
list: List all storage files
create: Create a storage file
    *Any*: File name (without extension)
exit: Exits CLI
help: This

In Open Store File:
    list: Lists storage items
    get: Get a item with key
        *Any*: Key name
    delete: Remove a key
        *Any*: Key Name
    set: Set or change a key's value
        *Any*: Key Name
        *Any*: Value
    back: Go back to root
""")
    if osf == "":
        match cmd:
            case "use":
                if len(args) <= 0:
                    print("File name or id required")
                else:
                    if os.listdir(".\\data\\").__contains__(args[0]) or os.listdir(".\\data\\").__contains__(args[0]+'.dat'):
                        osf = args[0].split(".dat")[0]
                        store.setProjectName(osf)
                    elif os.listdir(".\\data\\").__contains__(args[0]+'.dat'):
                        osf = args[0]
                        store.setProjectName(osf)
                    else:
                        try:
                            if abs(int(args[0])) <= len(os.listdir(".\\data\\")):
                                osf = os.listdir(".\\data\\")[abs(int(args[0]))].split(".dat")[0]
                                store.setProjectName(osf)
                        except ValueError:
                            print("Valid file name or id required")
                        except IndexError:
                            print("Valid file name or id required")
            case "list":
                index = 0
                print(f" {'ID': <3} | {'File name': <30} |")
                print(f"{'':-<39}")
                for i in os.listdir(".\\data\\"):
                    print(f" {index: <3} | {i: <30} |")
                    index += 1
            case "delete":
                if len(args) <= 0:
                    print("File name or id required")
                else:
                    phraseCommand("use "+args[0])
                    os.remove(".\\data\\"+osf+".dat")
                    print(f"Deleted {osf}.dat")
                    osf = ""
            case "create":
                if len(args) <= 0:
                    print("File name required")
                else:
                    osf = args[0]
                    store.setProjectName(osf)
                    store.save()
    else:
        match cmd:
            case "back":
                osf = ""
                store.setProjectName("general")
            case "list":
                jdata = store.openFile()
                print(f" {'Key Name': <30} | {'Value': <30} |")
                print(f"{'':-<66}")
                for i in jdata.keys():
                    print(f" {i: <30} | {jdata.get(i): <30} |")
            case "get":
                if len(args) <= 0:
                    print("Key name required")
                else:
                    jdata = store.openFile()
                    print(jdata.get(args[0]))
            case "delete":
                if len(args) <= 0:
                    print("Key name required to delete")
                else:
                    store.delete(args[0])
                    print("Deleted")
            case "set":
                if len(args) <= 1:
                    if len(args) == 1:
                        print("Key name and value required")
                    elif len(args) <= 2:
                        print("Key value required")
                else:
                    value = args[1]
                    try:
                        value = float(args[1])
                    except ValueError:
                        pass
                    try:
                        value = int(args[1])
                    except ValueError:
                        pass
                    store.save(args[0], value)
                    print(f"Set {args[0]} to {value}")


if len(sys.argv) <= 0:
    while True:
        end = "" if osf == "" else "\\"+osf
        cmd = input(f"storage{end}>")
        phraseCommand(cmd)
if sys.argv[0] == "/?" or sys.argv[0] == "-?":
    phraseCommand("help")
    exit(0)
