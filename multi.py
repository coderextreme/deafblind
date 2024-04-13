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
from collections import namedtuple



mp_hands = mp.solutions.hands.HandLandmark
poselm = mp.solutions.pose.PoseLandmark

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

pose = [
[poselm.NOSE, 0, "nose"],
[poselm.LEFT_EYE_INNER, 1, "l_eye_inner"],
[poselm.LEFT_EYE, 2, "l_eye"],
[poselm.LEFT_EYE_OUTER, 3, "l_eye_outer"],
[poselm.RIGHT_EYE_INNER, 4, "r_eye_inner"],
[poselm.RIGHT_EYE, 5, "r_eye"],
[poselm.RIGHT_EYE_OUTER, 6, "r_eye_outer"],
[poselm.LEFT_EAR, 7, "l_ear"],
[poselm.RIGHT_EAR, 8, "r_ear"],
[poselm.MOUTH_LEFT, 9, "l_mouth"],
[poselm.MOUTH_RIGHT, 10, "r_mouth"],
[poselm.LEFT_SHOULDER, 11, "l_shoulder"],
[poselm.RIGHT_SHOULDER, 12, "r_shoulder"],
[poselm.LEFT_ELBOW, 13, "l_elbow"],
[poselm.RIGHT_ELBOW, 14, "r_elbow"],
[poselm.LEFT_WRIST, 15, "l_wrist"],
[poselm.RIGHT_WRIST, 16, "r_wrist"],
[poselm.LEFT_PINKY, 17, "l_pinky"],
[poselm.RIGHT_PINKY, 18, "r_pinky"],
[poselm.LEFT_INDEX, 19, "l_index"],
[poselm.RIGHT_INDEX, 20, "r_index"],
[poselm.LEFT_THUMB, 21, "l_thumb"],
[poselm.RIGHT_THUMB, 22, "r_thumb"],
[poselm.LEFT_HIP, 23, "l_hip"],
[poselm.RIGHT_HIP, 24, "r_hip"],
[poselm.LEFT_KNEE, 25, "l_knee"],
[poselm.RIGHT_KNEE, 26, "r_knee"],
[poselm.LEFT_ANKLE, 27, "l_ankle"],
[poselm.RIGHT_ANKLE, 28, "r_ankle"],
[poselm.LEFT_HEEL, 29, "l_heel"],
[poselm.RIGHT_HEEL, 30, "r_heel"],
[poselm.LEFT_FOOT_INDEX, 31, "l_foot_index"],
[poselm.RIGHT_FOOT_INDEX, 32, "r_foot_index"]
]

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

MyLandmark = namedtuple('MyLandmark', 'x y z visibility')
# sendMessages()
class myClient(protocol.Protocol):
    def __init__(self):
        self.Impact = "Impact"
        self.Mocap = "Mocap"
        self.Cppon = "Cppon"
        self.sender = self.Mocap   # one of self.Mocap, self.Cppon, self.Impact.  Mocap is most performant

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
                self.sendAll(image, results.left_hand_landmarks, "l", mp_holistic.HAND_CONNECTIONS, hand)
                self.sendAll(image, results.right_hand_landmarks, "r", mp_holistic.HAND_CONNECTIONS, hand)
                self.sendAll(image, results.pose_landmarks, "p", mp_holistic.POSE_CONNECTIONS, pose)
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

    def sendAll(self, image, landmarks, suffix, connections, lmlist):
        # send lines to refresh the screen
        self.sendLines(connections, suffix)   # left hand
        # construct each time, because they disappear
        # self.constructPoints(landmarks, "_"+suffix, lmlist)
        # send coordinates
        self.sendPoints(image, landmarks, "_"+suffix, connections, lmlist)

    def constructPoints(self, landmarks, suffix, lmlist):
        if landmarks:
            if suffix in ("_t", "_c"):
                for landmark in range(len(landmarks.landmark)):
                    self.constructPoint(landmark, suffix, str(landmark))
            elif suffix in ("_p", "_l", "_r"):
                for landmark in lmlist:
                    self.constructPoint(landmark[0], suffix, landmark[2])
            if suffix in ("_p"):
                self.constructPoint(len(lmlist), suffix, "sacroiliac")
                self.constructPoint(len(lmlist)+1, suffix, "vc7")

    def sendPoints(self, image, landmarks, suffix, connections, lmlist):
        mp_drawing.draw_landmarks(image, landmarks, connections)
        if landmarks:
            if suffix in ("_t", "_c"):
                for landmark in range(len(landmarks.landmark)):
                    lmk = landmarks.landmark[landmark]
                    self.constructPoint(landmark, suffix, str(landmark))
                    self.sendPoint(lmk, landmark, suffix, str(landmark), image)
            elif suffix in ("_p"):
                for landmark in lmlist:
                    lmk = landmarks.landmark[landmark[0]]
                    # get rid of entire hands in pose landmarks
                    if landmark[0] < poselm.LEFT_WRIST or landmark[0] > poselm.RIGHT_THUMB:
                        self.constructPoint(landmark[0], suffix, landmark[2])
                        self.sendPoint(lmk, landmark[0], suffix, landmark[2], image)
            elif suffix in ("_l", "_r"):
                for landmark in lmlist:
                    lmk = landmarks.landmark[landmark[0]]
                    self.constructPoint(landmark[0], suffix, landmark[2])
                    self.sendPoint(lmk, landmark[0], suffix, landmark[2], image)
            if suffix in ("_p"):
                self.constructPoint(len(lmlist), suffix, "sacroiliac")
                lhlmk = landmarks.landmark[poselm.LEFT_HIP] 
                rhlmk = landmarks.landmark[poselm.RIGHT_HIP] 
                lmk = MyLandmark(
                       x= (lhlmk.x + rhlmk.x)/2,
                       y= (lhlmk.y + rhlmk.y)/2,
                       z= (lhlmk.z + rhlmk.z)/2,
                       visibility=(lhlmk.visibility + rhlmk.visibility)/2  )
                self.sendPoint(lmk, len(lmlist), suffix, "sacroiliac", image)

                self.constructPoint(len(lmlist)+1, suffix, "vc7")
                lslmk = landmarks.landmark[poselm.LEFT_SHOULDER] 
                rslmk = landmarks.landmark[poselm.RIGHT_SHOULDER] 
                lmk = MyLandmark(
                       x= (lslmk.x + rslmk.x)/2,
                       y= (lslmk.y + rslmk.y)/2,
                       z= (lslmk.z + rslmk.z)/2,
                       visibility=(lslmk.visibility + rslmk.visibility)/2  )
                self.sendPoint(lmk, len(lmlist)+1, suffix, "vc7", image)

    def sendMPLine(self, fr, to):
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
            if connection[0] == 23 and connection[1] == 24:
                pass
            elif connection[0] == 11 and connection[1] == 23:
                pass
            elif connection[0] == 11 and connection[1] == 12:
                pass
            elif connection[0] == 12 and connection[1] == 24:
                pass
            else:
                self.sendMPLine(f"{prefix}{connection[0]}", f"{prefix}{connection[1]}")
        if prefix in ("p"):
            self.sendMPLine(f"p33", f"p23") # patch the sacroiliac to the left hip
            self.sendMPLine(f"p33", f"p24") # patch the sacroiliac to the right hip
            self.sendMPLine(f"p34", f"p11") # patch the vc7 to the left shoulder
            self.sendMPLine(f"p34", f"p12") # patch the vc7 to the right shoulder
            self.sendMPLine(f"p33", f"p34") # patch the sacroiliac to vc7
            self.sendMPLine(f"p13", f"l0")  # patch the left elbow to the left wrist
            self.sendMPLine(f"p14", f"r0")  # patch the right elbow to the right wrist

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
        if prefix == "p_" and joint_string.startswith("l_"):
            prefix = ""
        elif prefix == "p_" and joint_string.startswith("r_"):
            prefix = ""
        cv2.putText(img=image, text=prefix+joint_string, org=(relative_x, relative_y), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0, 255, 0), thickness=1, lineType=cv2.LINE_AA)

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
