# sgpt --code "translate american sign language signing video to english textual paragraphs"
import cv2
import mediapipe as mp
import mediapipe.python.solutions.drawing_styles as ds
import typing
import numpy as np
from twisted.internet import reactor, threads
from twisted.internet.protocol import Protocol, ClientFactory
from queue import Queue
from twisted.internet.task import LoopingCall
from twisted.python import log



mp_hands = mp.solutions.hands.HandLandmark

hand = [[mp_hands.WRIST, "WRIST", "radiocarpal"],
[mp_hands.THUMB_CMC, "THUMB_CMC", "carpometacarpal_1"],
[mp_hands.THUMB_MCP, "THUMB_MCP", "metacarpophalangeal_1"],
[mp_hands.THUMB_IP, "THUMB_IP", "carpal_interphalangeal_1"],
[mp_hands.THUMB_TIP, "THUMB_TIP", "carpal_distal_phalanx_1"],
[mp_hands.INDEX_FINGER_MCP, "INDEX_FINGER_MCP", "metacarpophalangeal_2"],
[mp_hands.INDEX_FINGER_PIP, "INDEX_FINGER_PIP", "carpal_proximal_interphalangeal_2"],
[mp_hands.INDEX_FINGER_DIP, "INDEX_FINGER_DIP", "carpal_distal_interphalangeal_2"],
[mp_hands.INDEX_FINGER_TIP, "INDEX_FINGER_TIP", "carpal_distal_phalanx_2"],
[mp_hands.MIDDLE_FINGER_MCP, "MIDDLE_FINGER_MCP", "metacarpophalangeal_3"],
[mp_hands.MIDDLE_FINGER_PIP, "MIDDLE_FINGER_PIP", "carpal_proximal_interphalangeal_3"],
[mp_hands.MIDDLE_FINGER_DIP, "MIDDLE_FINGER_DIP", "carpal_distal_interphalangeal_3"],
[mp_hands.MIDDLE_FINGER_TIP, "MIDDLE_FINGER_TIP", "carpal_distal_phalanx_3"],
[mp_hands.RING_FINGER_MCP, "RING_FINGER_MCP", "metacarpophalangeal_4"],
[mp_hands.RING_FINGER_PIP, "RING_FINGER_PIP", "carpal_proximal_interphalangeal_4"],
[mp_hands.RING_FINGER_DIP, "RING_FINGER_DIP", "carpal_distal_interphalangeal_4"],
[mp_hands.RING_FINGER_TIP, "RING_FINGER_TIP", "carpal_distal_phalanx_4"],
[mp_hands.PINKY_MCP, "PINKY_MCP", "metacarpophalangeal_5"],
[mp_hands.PINKY_PIP, "PINKY_PIP", "carpal_proximal_interphalangeal_5"],
[mp_hands.PINKY_DIP, "PINKY_DIP", "carpal_distal_interphalangeal_5"],
[mp_hands.PINKY_TIP, "PINKY_TIP", "carpal_distal_phalanx_5"]]

# Load the MediaPipe Sign Language Detection model
mp_holistic = mp.solutions.holistic
holistic = mp_holistic.Holistic()

# Load the MediaPipe Drawing utils for visualization
mp_drawing = mp.solutions.drawing_utils

# load MedidPipe hands solutions

# Load the video file
# video_path = "path_to_video_file.mp4"
video_path = 0
cap = cv2.VideoCapture(video_path)

from twisted.internet import reactor, protocol

#class myServer(protocol.Protocol):
#    def dataReceived(self, data):
#        self.transport.write(data)

#class myServerFactory(protocol.Factory):
#    def buildProtocol(self, addr):
#        return myServer()

class myClientFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return myClient()

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed.")
        #reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("Connection lost.")
        #reactor.stop()

# sendMessages()
class myClient(protocol.Protocol):
    def startedEvent(self):
        print('started event')

    def performAnAction(self):
        # print('performed an action')
        if cap.isOpened():
            retval, frame = cap.read()
            if not retval:
                reactor.callLater(0, self.performAnAction)
            else:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Detect the signs in the frame
                results = holistic.process(frame_rgb)

                #signs = []
                #if results.pose_landmarks:
                #    sign = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_ELBOW].visibility
                #    signs.append(sign)

                for connection in mp_holistic.HAND_CONNECTIONS:
                    # print(connection)
                    self.bufferMessage(f"F:{connection[0]}")
                    self.bufferMessage(f"T:{connection[1]}")
                if results.left_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
                    for landmark in hand:
                        lmk = results.left_hand_landmarks.landmark[landmark[0]]
                        self.printHand(lmk, "l_"+landmark[2], frame)
                if results.right_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
                    for landmark in hand:
                        lmk = results.right_hand_landmarks.landmark[landmark[0]]
                        self.printHand(lmk, "r_"+landmark[2], frame)
                if results.pose_landmarks:
                    mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
                    for landmark in range(len(results.pose_landmarks.landmark)):
                        lmk = results.pose_landmarks.landmark[landmark]
                        self.printHand(lmk, str(landmark), frame)

                # Display the frame
                cv2.imshow("Sign Language Detection", frame)
                # Break the loop if 'q' is pressed
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.bufferSend()
                    print("Stopping")
                    reactor.stop()
        else:
            print("Video died")
        self.bufferSend()
        reactor.callLater(0, self.performAnAction)
        # tail "recursion"
        # reactor.callLater(0, self.performAnAction)

    def connectionMade(self):
        self.sendMessage("Marker: Start")  # Send marker for the first frame
        self.buffer = []
        self.runRecognizer()


    def sendMessage(self, message):
        self.transport.write(message.encode())
        # self.transport.write(message)

    def bufferSend(self):
        message = "\n".join(self.buffer)+"\n"
        # print(message)
        self.sendMessage(message)
        self.buffer = []

    def bufferMessage(self, message):
        self.buffer.append(message);

    def printHand(self, lmk, joint_string: str, frame):

        self.bufferMessage(f"J:{joint_string}")
        # print(lmk)
        x = lmk.x
        y = lmk.y
        z = lmk.z
        v = lmk.visibility
        shape = frame.shape
        self.bufferMessage(f"X:{x}")
        self.bufferMessage(f"Y:{y}")
        self.bufferMessage(f"Z:{z}")
        relative_x = int(x * shape[1])
        relative_y = int(y * shape[0])
        relative_z = int(z * shape[2])
        self.bufferMessage(f"XR:{relative_x}")
        self.bufferMessage(f"YR:{relative_y}")
        self.bufferMessage(f"ZR:{relative_z}")
        cv2.putText(img=frame, text=joint_string, org=(relative_x, relative_y), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(255, 0, 0), thickness=1, lineType=cv2.LINE_AA)

    def runRecognizer(self):
        certainAmount = 5.0  # this is in seconds
        self.bufferMessage("S:D")
        reactor.callLater(0, self.performAnAction)
        # self.transport.loseConnection()

from twisted.internet import task

reactor.connectTCP('127.0.0.1', 3000, myClientFactory())
# reactor.listenTCP(3002, myServerFactory())
reactor.run()
cap.release()
cv2.destroyAllWindows()

# # Convert the detected signs to English textual paragraphs
# textual_paragraphs = []
# current_paragraph = ""
# for sign in signs:
#    if sign > 0.5:
#        current_paragraph += " "
#    else:
#        current_paragraph += "."
#        textual_paragraphs.append(current_paragraph)
#        current_paragraph = ""
#
# # Print the English textual paragraphs
# for paragraph in textual_paragraphs:
#    print(paragraph)
