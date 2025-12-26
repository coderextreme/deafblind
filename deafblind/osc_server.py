from pythonosc import dispatcher
from pythonosc import osc_server

def print_handler(unused_addr, *args):
    print(f'Received: {args}')

disp = dispatcher.Dispatcher()
disp.map('/VMC/Ext/Bone/Pos', print_handler)

server = osc_server.BlockingOSCUDPServer(('127.0.0.1', 39539), disp)
print('OSC Server listening on port 39539...')
server.serve_forever()
