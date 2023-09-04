import time

import cv2
import mediapipe as mp
import numpy as np
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

MARGIN = 10  # pixels
FONT_SIZE = 1
FONT_THICKNESS = 1
HANDEDNESS_TEXT_COLOR = (88, 205, 54) # vibrant green

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode


def printHand(result: mp.tasks.vision.HandLandmarkerResult, category, frame: mp.Image):
    # Note, google, 0 index is Right, and 1 index is left.  Obviously, you're taking the camera viewpoint
    print("Index:", category.index, ", Display name:", category.display_name, ", Category name:", category.category_name);
    #hand_landmarks_list = result.hand_landmarks
    #for idx in range(len(hand_landmarks_list)):
    #    hand_landmarks = hand_landmarks_list[idx]
    #    for lmk in hand_landmarks:
    #        print(lmk.x, lmk.y, lmk.z, lmk.visibility, lmk.presence)

def print_result(result: mp.tasks.vision.HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    print('hand landmarker result: {}'.format(result))
    if len(result.handedness) > 0:
        #print(result.handedness[0])
        printHand(result, result.handedness[0][0], output_image)
        if len(result.handedness) > 1:
            #print(result.handedness[1])
            printHand(result, result.handedness[1][0], output_image)

    mp_drawing.draw_landmarks(output_image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
    mp_drawing.draw_landmarks(output_image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
    cv2.imshow('Frame', output_image)
            x = lmk.x
            y = lmk.y
            z = lmk.z
            shape = image.shape
            relative_x = int(x * shape[1])
            relative_y = int(y * shape[0])
            lefthandstr = "l_"+landmark[1]
            cv2.putText(img=image, text=lefthandstr, org=(relative_x, relative_y), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.3, color=(255, 0, 0), thickness=5, lineType=cv2.LINE_AA)

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path='./hand_landmarker.task'),
    running_mode=VisionRunningMode.LIVE_STREAM,
    # num_hands=2,
    result_callback=print_result)

with HandLandmarker.create_from_options(options) as landmarker:
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
