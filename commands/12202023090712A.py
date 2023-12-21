#dget
import sys
if sys.argv[0] == "/?" or sys.argv[0] == "-?":
    print("""dget - Downloading Get
Downloads remote files
------------
Arguments:
    1: Absolute URL to the file 
    2: Downloaded file name
""")
    exit(0)
import helpers.h_require
if not helpers.h_require.requireCheck({"requests", "tqdm"}, True):
    exit(0)
import requests, time
from tqdm import tqdm
sys.argv.pop(0)
match len(sys.argv):
    case 0:
        print("URL and File Name required")
        exit(1)
    case 1:
        print("File Name required")
        exit(1)
url = str(sys.argv[0])
outName = str(sys.argv[1])
response: requests.Response
try:
    print("Requesting...")
    response = requests.get(url, stream=True)
except ConnectionError as e:
    print(f"[0x02] Connection Error: {e}")
    exit(2)
except Exception as e:
    print(f"[0x03] Unknown Error: {e}")
    exit(3)
print("Received")
total_size_in_bytes = int(response.headers.get('content-length', 0))
realSize = 0
block_size = 1024 # 1 Kibibyte
if total_size_in_bytes == 0:
    with open(outName, 'wb') as file:
        for data in response.iter_content(block_size):
            realSize += len(data)
            file.write(data)
else:
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    total_size_in_bytes = 0
    with open(outName, 'wb') as file:
        for data in response.iter_content(block_size):
            realSize += len(data)
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print("[0x04] Something went wrong")
print("Download Complete, status code: "+str(response.status_code))
print("Downloaded "+str(realSize)+" Bytes")
