Open Source Control/Virtual Motion Capture https://protocol.vmc.info/english.html

Protocol Experiments with MediaPipe/Holistic and OpenCV.
---------------------------------------------------------------------------------------------------------------
How to reconstruct the venv311 folder in the zip:

Plug in webcam and open lens

In Developer Powershell, run:

Optional:

PS C:\> mkdir deafblind

Required:

PS C:\> cd deafblind
PS C:\deafblind> py -3.11 -m venv venv311
PS C:\deafblind> venv311\Scripts\activate
PS C:\deafblind> pip install numpy==1.24.3
PS C:\deafblind> pip install opencv-python==4.8.1.78
PS C:\deafblind> pip install mediapipe==0.10.14
PS C:\deafblind> pip install python-osc
----------------------------------------------------------------------------------------------------------
Run the server in PowerShell:

PS C:\> cd deafblind
PS C:\deafblind> venv311\Scripts\activate
PS C:\deafblind> python .\osc_server.py

Press CTRL-C in osc_server.py window to exit
----------------------------------------------------------------------------------------------------------
Run the client in PowerShell:

PS C:\> cd deafblind
PS C:\deafblind> venv311\Scripts\activate
PS C:\deafblind> python .\osc.py Bob

Wait for video to come up, check other Powershell.

Wave to yourself!  See server window go wild!

Press ESC key in video to exit
