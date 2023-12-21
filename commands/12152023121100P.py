import sys, os
args = sys.argv
args.pop(0)
try:
    os.system('ping '+' '.join(args))
except KeyboardInterrupt:
    exit()