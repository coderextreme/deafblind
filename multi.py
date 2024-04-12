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
import time



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
holistic = mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5)

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
        # reactor.stop()

# sendMessages()
class myClient(protocol.Protocol):
    def __init__(self):
        self.Impact = "Impact"
        self.Mocap = "Mocap"
        self.Cppon = "Cppon"
        self.sender = self.Impact   # one of self.Mocap, self.Cppon, self.Impact

        self.sequenceno = -1
        self.connection_counter = 0
        self.header = ""

        recipients = "*"
        self.header += "{"
        self.header += "{"
        self.header += recipients
        self.header += "}"
        self.header += "}"

        self.header += "{"
        self.header += self.sender
        self.header += "}"

        self.footer = ""
        error = ""
        self.footer += "{"
        self.footer += error
        self.footer += "}"

        language = "en"
        self.footer += "{"
        self.footer += language
        self.footer += "}"

        nick = self.sender+"User"   # one of MocapUser, CpponUser, ImpactUser
        self.footer += "{"
        self.footer += nick
        self.footer += "}"

    def startedEvent(self):
        print('started event')

    def performAnAction(self):
        # print('performed an action')
        if cap.isOpened():
            retval, frame = cap.read()
            if not retval:
                reactor.callLater(0, self.performAnAction)
            else:
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Detect the signs in the frame
                results = holistic.process(image)

                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                #signs = []
                #if results.pose_landmarks:
                #    sign = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_ELBOW].visibility
                #    signs.append(sign)

                # Comment out these lines as desired.  Please don't delete them
                self.sendAll(image, results.left_hand_landmarks, "l", mp_holistic.HAND_CONNECTIONS)
                self.sendAll(image, results.right_hand_landmarks, "r", mp_holistic.HAND_CONNECTIONS)
                self.sendAll(image, results.pose_landmarks, "p", mp_holistic.POSE_CONNECTIONS)
                #self.sendAll(image, results.face_landmarks, "t", mp_holistic.FACEMESH_TESSELATION)
                #self.sendAll(image, results.face_landmarks, "c", mp_holistic.FACEMESH_CONTOURS)

                # Display the frame
                cv2.imshow("Sign Language Detection", image)
                # Break the loop if ESC is pressed
                if cv2.waitKey(30) == 27:
                    self.bufferSend()
                    print("Stopping")
                    reactor.stop()
        else:
            print("Video died")
        self.bufferSend()
        reactor.callLater(0, self.performAnAction)

    def sendAll(self, image, landmarks, suffix, connections):
        # send lines to refresh the screen
        self.sendLines(connections, suffix)   # left hand
        # construct each time, because they disappear
        # self.constructPoints(landmarks, "_"+suffix)
        # send coordinates
        self.sendPoints(image, landmarks, "_"+suffix, connections)

    def constructPoints(self, landmarks, suffix):
        if landmarks:
            if suffix in ("_p", "_t", "_c"):
                for landmark in range(len(landmarks.landmark)):
                    lmk = landmarks.landmark[landmark]
                    self.constructPoint(landmark, suffix, str(landmark))
            else:
                for landmark in hand:
                    lmk = landmarks.landmark[landmark[0]]
                    self.constructPoint(landmark[0], suffix, landmark[2])

    def sendPoints(self, image, landmarks, suffix, connections):
        mp_drawing.draw_landmarks(image, landmarks, connections)
        if landmarks:
            if suffix in ("_p", "_t", "_c"):
                for landmark in range(len(landmarks.landmark)):
                    lmk = landmarks.landmark[landmark]
                    self.constructPoint(landmark, suffix, str(landmark))
                    self.sendPoint(lmk, landmark, suffix, str(landmark), image)
            else:
                for landmark in hand:
                    lmk = landmarks.landmark[landmark[0]]
                    self.constructPoint(landmark[0], suffix, landmark[2])
                    self.sendPoint(lmk, landmark[0], suffix, landmark[2], image)

    def sendMPLines(self, fr, to):
        # print(fr, to)
        if self.sender == self.Cppon:
            variable = f"Line{self.connection_counter}"
            self.bufferMessage(f"Line {variable} = Line();")
            self.bufferMessage(f'{variable}.setFrom(CString("{fr}"));')
            self.bufferMessage(f'{variable}.setTo(CString("{to}"));')
            self.connection_counter = self.connection_counter + 1
        elif self.sender == self.Mocap:
            self.bufferMessage(f'F:{fr}')
            self.bufferMessage(f'T:{to}')
            self.connection_counter = self.connection_counter + 1
        elif self.sender == self.Impact:
            variable = f"{self.connection_counter}"
            # self.bufferMessage(f'SEGMENT|{variable}|DELETE|{fr}|{to}')
            self.bufferMessage(f'SEGMENT|{variable}|INSERT|{fr}|{to}')
            self.bufferMessage(f'SEGMENT|{variable}|UPDATE|{fr}|{to}')
            self.connection_counter = self.connection_counter + 1

        if self.connection_counter < 0:  # wrap around, I hope
            self.connection_counter = 0

    def sendLines(self, connections, prefix):
        for connection in connections:
            self.sendMPLines(f"{prefix}{connection[0]}", f"{prefix}{connection[1]}")

    def connectionMade(self):
        self.sendMessage("Marker: Start")  # Send marker for the first frame
        self.buffer = []
        self.runRecognizer()


    def sendMessage(self, message):
        entiremessage = ""

        entiremessage += self.header

        timestamp = time.time()
        entiremessage += "{"
        entiremessage += str(int(timestamp))
        entiremessage += "}"

        self.sequenceno += 1
        entiremessage += "{"
        entiremessage += str(self.sequenceno)
        entiremessage += "}"

        entiremessage += self.footer
        entiremessage += message
        self.transport.write(entiremessage.encode())
        # self.transport.write(message)

    def bufferSend(self):
        message = " ".join(self.buffer)+"\n"
        # print(message)
        self.sendMessage(message)
        self.buffer = []

    def bufferMessage(self, message):
        # print(f"{message}\n");
        self.buffer.append(message);

    def constructMPPoint(self, landmark, suffix, defn):
        if self.sender == self.Cppon:
            ptid = f"{landmark}{suffix}"
            self.bufferMessage(f"Point Point{ptid} = Point();")
            self.bufferMessage(f'Point{ptid}.setDEF(CString("{defn}");')
        elif self.sender == self.Mocap:
            self.bufferMessage(f"J:{defn}")
            self.bufferMessage(f"L:{landmark}")
        elif self.sender == self.Impact:
            prefix = suffix[1:]
            ptid = f"{prefix}{landmark}"
            self.bufferMessage(f'NODE|{ptid}|INSERT')


    def constructPoint(self, landmark, suffix, joint_string: str):
        prefix = suffix[1:]
        self.constructMPPoint(landmark, suffix, f"{prefix}_{joint_string}")

    def sendMPPoint(self, landmark, suffix, x, y, z):
        if self.sender == self.Cppon:
            xyz = "{"+f"{x}, {y}, {z}"+"}"
            ptid = f"{landmark}{suffix}"
            self.bufferMessage(f"Point{ptid}.setPoint(new float[]{xyz});")
        elif self.sender == self.Mocap:
            self.bufferMessage(f"X:{x}")
            self.bufferMessage(f"Y:{y}")
            self.bufferMessage(f"Z:{z}")
        elif self.sender == self.Impact:
            x = x*10-5
            y = y*10-5
            y = -y
            z = z*10
            prefix = suffix[1:]
            ptid = f"{prefix}{landmark}"
            self.bufferMessage(f'NODE|{ptid}|UPDATE|1|1|1|1|{x}|{y}|{z}|0.0|0.0|0.0')

    def sendPoint(self, lmk, landmark, suffix, joint_string: str, image):

        # print(lmk)
        
        x = round(lmk.x, 5)
        y = round(lmk.y, 5)
        z = round(lmk.z, 5)
        v = lmk.visibility
        shape = image.shape

        self.sendMPPoint(landmark, suffix, x, y, z)
        # print(v)
        relative_x = int(x * shape[1])
        relative_y = int(y * shape[0])
        #relative_z = int(z * shape[2])
        #self.bufferMessage(f"XR:{relative_x}")
        #self.bufferMessage(f"YR:{relative_y}")
        #self.bufferMessage(f"ZR:{relative_z}")
        prefix = suffix[1:]+"_"
        cv2.putText(img=image, text=prefix+joint_string, org=(relative_x, relative_y), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(255, 0, 0), thickness=1, lineType=cv2.LINE_AA)

    def runRecognizer(self):
        certainAmount = 5.0  # this is in seconds
        if self.sender == self.Cppon:
            self.bufferMessage("X3D X3D0 = X3D();")
        reactor.callLater(0, self.performAnAction)
        # self.transport.loseConnection()

from twisted.internet import task

reactor.connectTCP('127.0.0.1', 8180, myClientFactory())
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
