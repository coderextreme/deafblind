# sgpt --code "translate american sign language signing video to english textual paragraphs"
import cv2
import numpy as np
import mediapipe as mp

# Load the MediaPipe Sign Language Detection model
mp_holistic = mp.solutions.holistic
holistic = mp_holistic.Holistic()

# Function to extract keypoints from the detected hand landmarks
def extract_keypoints(results):
    keypoints = []
    for data_point in results.landmark:
        keypoints.append([data_point.x, data_point.y, data_point.z])
    return keypoints

# Function to convert keypoints to text
def keypoints_to_text(keypoints):
    text = ""
    for point in keypoints:
        text += f"{point[0]} {point[1]} {point[2]}\n"
    return text

# Load the video file
cap = cv2.VideoCapture(0)

# Create a VideoWriter object to save the output video
fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter('output_video.avi', fourcc, 30.0, (640, 480))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect hand landmarks
    results = holistic.process(image)

    # Extract keypoints from the detected hand landmarks
    keypoints = extract_keypoints(results)

    # Convert keypoints to text
    text = keypoints_to_text(keypoints)

    # Draw the keypoints on the frame
    mp_drawing = mp.solutions.drawing_utils
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

    # Write the frame with keypoints to the output video
    # out.write(image)

    # Display the frame with keypoints
    cv2.imshow('Sign Language Video', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture and VideoWriter objects
cap.release()
out.release()

# Close all OpenCV windows
cv2.destroyAllWindows()
