import socketio

sio = socketio.Client()

@sio.event
def connect():
    print('connected to server')

@sio.event
def disconnect():
    print('disconnected from server')

if __name__ == '__main__':
    # sio.connect('http://localhost:5000')
    sio.connect("ws://localhost:5000/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2ODE2NjIxMDUsImlhdCI6MTY4MTU3NTcwNSwic3ViIjoib21hcmdjIiwicGF5bG9hZCI6eyJkZXNjcmlwY2lvbiI6ImN1YWxxdWllcl9jb3NhIn19.iel7b635_BZwaSM7IaWyEG7MNZEerxnMGSGXLgQKzoM")
    # sio.emit('event', {'key': 'value'})
    sio.emit({"action": "message", "message": {"destinatario": "diego", "contenido": "Hola, ¿todo bien?"}})
    
    # disconnect from server and end script
    sio.disconnect()
    # sio.wait()