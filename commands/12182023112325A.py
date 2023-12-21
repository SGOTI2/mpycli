import helpers.h_require
import helpers.h_store
helpers.h_store.setProjectName("12182023112325A-CAM")
if not helpers.h_require.requireCheck({'opencv-python'}):
    exit(1)
try:
    import cv2
except ImportError:
    print("[0x01] Something went wrong")
    exit(1)
camID = helpers.h_store.get("camID", -1)
print(f"Connecting to camera {camID}")
vid = cv2.VideoCapture(camID, cv2.CAP_DSHOW)
if vid is None or not vid.isOpened():
    print("[0x02] Default ID failed Checking first 10 ids")
    camID = 0
    for i in range(10):
        vid = cv2.VideoCapture(camID)
        if vid is None or not vid.isOpened():
            print(f"A camera was not found for this cap id ({camID})")
            camID += 1
            continue
        else:
            print(f"Camera Found id: {camID}")
            helpers.h_store.save("camID", camID)
            print("Camera ID Saved")
            break
if vid is None or not vid.isOpened():
    print("[0x03] Failed to find valid camera")
    exit(2)
print("Press 'q' to quit")
while(True):
    ret, frame = vid.read()
    cv2.imshow('Camera', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
vid.release()
cv2.destroyAllWindows() 