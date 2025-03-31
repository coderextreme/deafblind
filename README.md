Quick start:

Run:
```
git clone https://coderextreme.net/coderextreme/deafblind
cd deafblind
bash install.sh
```
in a terminal

Here's what to try.

READ install.txt for installation

RUN install.bat for installation (in Bash)

Start up a server in one terminal with

$ source -venv-/Scripts/activate

replace -venv- with your python virtual environment

$ python twistedserver.py

Start up the cient in another terminal and use

$ source -venv-/Scripts/activate

$ python recognizehands.py

Watch video and skeleton from webcam/MediaPipe/OpenCV and server stream!

John

Notes.  I don't know about distribution of these, so I'm not checking them in.  I probably had the wrong version of mediapipe (see links for correct version).

===

gesture_recognizer.task

From: https://colab.research.google.com/github/googlesamples/mediapipe/blob/main/examples/gesture_recognizer/python/gesture_recognizer.ipynb#:~:text=%21wget,-q%20https%3A%2F%2Fstorage.googleapis.com%2Fmediapipe-models%2Fgesture_recognizer%2Fgesture_recognizer%2Ffloat16%2F1%2Fgesture_recognizer.task

hand_landmarker.task

From: https://colab.research.google.com/github/googlesamples/mediapipe/blob/main/examples/hand_landmarker/python/hand_landmarker.ipynb#:~:text=%21pip%20install%20-q%20mediapipe%3D%3D0.10.0%20Then%20download%20an%20off-the-shelf,this%20model%20bundle.%20%5B%20%5D%20%21wget%20-q%20https%3A%2F%2Fstorage.googleapis.com%2Fmediapipe-models%2Fhand_landmarker%2Fhand_landmarker%2Ffloat16%2F1%2Fhand_landmarker.task

Are for the next version of media pipe.  See backup folder

backup/best.py
backup/original.py
backup/dustbin.py

Good luck with that, I couldn't get video/recognition working

=============
```
Notes on protocol (possibly out of date).

I am proposing a new mocap format that doesn’t need a hierarchy, and can do streaming, graph or grid data.
S:structure of data, G for grid, H for tree, D for D for DAG, C for cycles
V: name or id of structure 
F: from joint name and/or id
T: to joint name and/or id

O: out name
B: out data (beginning)
I: in name
E: in data  (ending)...etc. 

The animation is done like:
J:Joint id or name
L:landmark, left(l), right (r) or pose(p)
C:Joint class or type (may change)
A:Joint alias or DEF (optional)
X:X location, unit (unit may be defaulted, no unit for scaling)
Y:Y location, unit (ditto)
Z:Z location, unit (ditto)
T:frame or time, unit (ditto)...etc.

To remove joint, bones or routes:
-V: remove structure  
-J: remove joint 
-F: from joint name and/or id
-T: to joint name and/or id

Later, I will provide 4 data points per joint over time, for impact simulator I/O grid
J: Joint, as above
U: up data
D: down data
R: right data
L?: left data
```

Plus ways to remove data by adding a - in front or behind the label and a leading or a trailing + to add data (to a tuple)
This needs to be generalized. Think how to do hypergraphs. More verbose would be an option,
IDK, i don’t want to reinvent a document format.

Good question about BVH!  I am proposing a new mocap format that doesn’t need a hierarchy, and can do streaming, graph or grid data.

Inspired by Katy Schildmeyer's Joint Location format.
