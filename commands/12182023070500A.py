import sys
import helpers.h_store
import helpers.h_require
helpers.h_store.setProjectName("12182023070500A-CLIC")
# Set time between clicks (Secs) set to aprox. 0 for fastest 
KEY_INPUT_DELAY = float(helpers.h_store.get("key_input_delay", 0.001, True))
# Amount of clicks to preform before checking for exit keys (Use to speed up program if KEY_INPUT_DELAY is <= 0 (set EXIT_POLL_ITER higher))
EXIT_POLL_ITER = int(helpers.h_store.get("exit_poll_interval", 1, True))

if len(sys.argv) > 1:
    if sys.argv[1] == "-kid":
        if len(sys.argv) > 2:
            KEY_INPUT_DELAY = float(sys.argv[2])
            helpers.h_store.save("key_input_delay",KEY_INPUT_DELAY)
            print("Saved Key Input Delay")
        else:
            print("Value Required for Key Input Delay (Secs.)")

# Import modules (Install if not installed)
if not helpers.h_require.requireCheck({'keyboard','pyautogui','pillow'}):
    exit(1)
try:
    import pyautogui
    from keyboard import is_pressed
    from time import sleep, time
except ImportError:
    print("[0x01] Something went wrong")
    exit(1)
cps = str(1 / KEY_INPUT_DELAY) if KEY_INPUT_DELAY > 0 else "N/A"
print(f"Set to {cps} CPS")
print("Press 1 & 3 (at the same time) to start, esc to cancel")
while True:
    try:
        if is_pressed("esc"):
            exit(0)
        elif is_pressed("1") and is_pressed("3"):
            break
        sleep(0.1)
    except KeyboardInterrupt:
        exit(0)

pyautogui.PAUSE = 0

print("Starting ....")
while True:
    if is_pressed("esc"):
        break
    for i in range(EXIT_POLL_ITER):
        stT = time()
        pyautogui.leftClick()
        curT = time()
        if KEY_INPUT_DELAY > 0 and KEY_INPUT_DELAY - (curT - stT) >= 0:
            sleep(KEY_INPUT_DELAY - (curT - stT))
print("Finished!")