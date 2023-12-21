import json, os, sys

global _projectName
_projectName = "general"
def setProjectName(name: str):
    global _projectName
    _projectName = name
    if sys.argv.__contains__("--storage"):
        print("Storage file is "+name+".dat")
def openFile():
    data = "{ }"
    try:
        if os.path.exists(".\\data\\"):
            with open(".\\data\\"+_projectName+".dat", "r") as f:
                data = f.read()
        else:
            os.mkdir(".\\data\\")
    except FileNotFoundError:
        data = "{ }"
    return json.loads(data)
def get(name: str, default = None, setNotFound = False):
    try:
        return openFile()[name]
    except KeyError:
        if setNotFound:
            save(name, default)
        return default
def delete(name: str):
    try:
        data = openFile()
        del data[name]
        writing = json.dumps(data)
        if not os.path.exists(".\\data\\"):
            os.mkdir(".\\data\\")
        with open(".\\data\\"+_projectName+".dat", "w") as f:
            f.write(writing)
    except:
        return
def save(name: str = None, value = None):
    writing = "{ }"
    if name != None and value != None:
        data = openFile()
        data[name] = value
        writing = json.dumps(data)
    elif name == None and value == None:
        pass
    else:
        return
    if not os.path.exists(".\\data\\"):
        os.mkdir(".\\data\\")
    with open(".\\data\\"+_projectName+".dat", "w") as f:
        f.write(writing)