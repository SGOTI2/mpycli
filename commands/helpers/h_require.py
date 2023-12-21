import sys
import subprocess
python = sys.executable
try:
    import pkg_resources
except ImportError:
    print("[WARNING][0x90] pkg_resources not found! attempting to install")
    subprocess.check_call([python, '-m', 'pip', 'install', "setuptools"])
    try:
        import pkg_resources
    except:
        print("[CRITICAL][0x9A] pkg_resources not found! Python may be installed improperly, try reinstalling")
        exit(1)
    print("[LOG][1x90] Fixed")
def requireCheck(requirements,required=True):
    required = requirements
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed

    if missing:
        print("To run this command external modules will need to be installed")
        yni = input("install?[Y,N]")
        if yni.lower() == "y":
            print("Installing")
            subprocess.check_call([python, '-m', 'pip', 'install', *missing])
            print("Finished Installing, you may need to recall the command")
        elif required:
            print("This command will not run until you install these modules")
            return False
        else:
            return False
    return True
