import cv2
import sys

i = 0
found = False
for i in range(4):
        capture = cv2.VideoCapture(i)
        if not capture:
            print("UNABLE TO CAPTURE CAMERA")
        else:
            found = True
            print(f"taken camera from index: {i}")
            break

if found == False:
    print("!!! No camera was found.")
    sys.exit()

# capture = cv2.VideoCapture()
capture.open(0)
while capture.isOpened():
    retval, frame = capture.read()
    if retval:
        cv2.imshow("Sign Language Detection", frame)
        if cv2.waitKey(30) == 27:  # ESC
            capture.release()
            cv2.destroyAllWindows()
            break
    else:
        break
