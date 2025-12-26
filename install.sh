py -m venv venv
source venv/Scripts/activate
python -m pip install --upgrade pip 
pip install twisted
pip install opencv-python
pip install mediapipe
pip install "python-socketio[client]"
python sockio.py Holger 0.0 1.0 0.0 0.0 0.0 0.0 # red green blue offset_z offset_y offset_z
