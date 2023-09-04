# sgpt --code "translate americal sign language signing video to english textual paragraphs"
import cv2
import mediapipe as mp

# Load the MediaPipe Sign Language Detection model
mp_holistic = mp.solutions.holistic
holistic = mp_holistic.Holistic()

# Load the MediaPipe Drawing utils for visualization
mp_drawing = mp.solutions.drawing_utils

# Load the video file
video_path = "path_to_video_file.mp4"
video_path = 0
cap = cv2.VideoCapture(video_path)

# Initialize an empty list to store the detected signs
signs = []

# Process each frame in the video
while cap.isOpened():
    # Read the current frame
    success, image = cap.read()
    if not success:
        break

    # Convert the image to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Detect the signs in the image
    results = holistic.process(image_rgb)

    # Draw the signs on the image
    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)

    # Extract the detected signs from the results
    if results.pose_landmarks:
        sign = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_ELBOW].visibility
        signs.append(sign)

    # Display the image
    cv2.imshow("Sign Language Detection", image)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()

# Convert the detected signs to English textual paragraphs
textual_paragraphs = []
current_paragraph = ""
for sign in signs:
    if sign > 0.5:
        current_paragraph += " "
    else:
        current_paragraph += "."
        textual_paragraphs.append(current_paragraph)
        current_paragraph = ""

# Print the English textual paragraphs
for paragraph in textual_paragraphs:
    print(paragraph)
