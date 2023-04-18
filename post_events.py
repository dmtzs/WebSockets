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
    tokenp1 = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    tokenp2_1 = "eyJleHAiOjE2ODE2NjIxMDUsImlhdCI6MTY4MTU3NTcwNSwic3ViIjoib21"
    tokenp2 = tokenp2_1 + "hcmdjIiwicGF5bG9hZCI6eyJkZXNjcmlwY2lvbiI6ImN1YWxxdWllcl9jb3NhIn19"
    tokenp3 = "iel7b635_BZwaSM7IaWyEG7MNZEerxnMGSGXLgQKzoM"
    sio.connect(f"ws://localhost:5000/{tokenp1}.{tokenp2}.{tokenp3}")
    # sio.emit('event', {'key': 'value'})
    sio.emit({"action": "message","topic_name": "noticias","content": "Content of the message"})
    
    # disconnect from server and end script
    sio.disconnect()
    # sio.wait()