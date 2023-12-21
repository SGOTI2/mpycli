import sys
sys.argv.pop(0)
if len(sys.argv) >= 1:
    if sys.argv[0] == "server":
        import server
        exit(0)
import client
exit(0)