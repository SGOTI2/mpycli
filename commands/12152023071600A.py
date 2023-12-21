import sys, os, re
args = sys.argv
args.pop(0)
if len(args) < 1:
    print("Command Required")
    exit()
path = os.getenv('APPDATA')+"\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\mpycli_run.bat"
if args[0] == "delete" or args[0] == "-d":
    if os.path.exists(path):
        os.remove(path)
        print("Deleted all startup items")
    else:
        print("Nothing in startup")
    exit()
if args[0] == "list" or args[0] == "-l":
    if os.path.exists(path):
        with open(path, "r") as f:
            tex = f.read()
        tex = tex.replace("@echo off\n","")
        tex = re.sub(r'.+py" ', '', tex)
        print(tex)
    else:
        print("Nothing in startup")
    exit()
if not os.path.exists(path):
    writing = "@echo off\n"
else:
    writing = ""
writing += "python.exe \""+os.getcwd()+"\\app.py\" "+(' '.join(args))+"\n"
with open(path, "a") as f:
    f.write(writing)
print("Added '"+' '.join(args)+"' to startup")
