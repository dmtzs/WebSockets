try:
    import jwt
    import json
    import asyncio
    import traceback
    import websockets
except ImportError as err_imp:
    print(f"The following import error occurred: {err_imp}")

# Definir una clase para manejar las conexiones WebSocket
class WebSocketHandler:
    def __init__(self, websocket):
        self.websocket = websocket
        self.username = None

    # Función para enviar mensajes a otros usuarios
    async def send_message(self, recipient:str, message:dict[str, str]) -> None:
        """
        Method to send a message to a recipient.

        :param recipient: The recipient username.
        :param message: The message to send in dict format.
        :return: None
        """
        if recipient in CONNECTED_USERS:
            recipient_socket = CONNECTED_USERS[recipient]
            await recipient_socket.websocket.send(json.dumps(message))
            print(f"Message sent to destinatary: {recipient}: {message}")
        else:
            print(f"Destinatary {recipient} not connected, message stored to be delivered later.")
            PENDING_MESSAGES[recipient].append(message)

    async def authenticate(self, token: str) -> bool:
        """
        Method to authenticate the user.

        :param token: The user token.
        :return: True if the token is valid, False otherwise.
        """
        try:
            # Verify the user token.
            payload = jwt.decode(token, 'B7PwGjhYohg', algorithms=['HS256'])
            self.username = payload['sub']
            CONNECTED_USERS[self.username] = self.websocket
            print(f"Connected user: {self.username}.")

            # TODO: Verify if there are pending messages.

            return True
        except:
            # Si el token no es válido.
            print("Invalid token")
            return False

    async def subscribe(self, channel):
        """Función para suscribirse a un canal o tema.  """
        # Verificar que el canal exista y el usuario tenga permiso para suscribirse.
        if channel in CHANNELS and self.username in CHANNELS[channel]:
            # Agregar al usuario a la lista de usuarios suscritos a este canal.
            CHANNELS[channel].append(self.username)
            return True
        else:
            return False

    # Función para procesar mensajes entrantes
    async def handle_message(self, info_message:dict|None=None) -> None:
        """
        Method to handle incoming messages and be sent to the correct destinataries.

        :param info_message: The message to be sent.
        :return: None
        """
        print("handle_message -> ", info_message["message"])
        if info_message is not None:
            topic_name = info_message["topic"]
            print("Info message not none")
            if topic_name in CHANNELS["public"]["topicos"] and self.username in CHANNELS["public"]["usuarios"]:
                print("entro a publico")
                for recipient in CHANNELS["public"]["usuarios"]:
                    message_complete = {
                        "topic_name": topic_name,
                        "content": info_message["message"]
                    }
                    await self.send_message(recipient=recipient, message=message_complete)
            
            elif topic_name in CHANNELS["private"]["topicos"] and self.username in CHANNELS["private"]["usuarios"]:
                for recipient in CHANNELS["private"]["usuarios"]:
                    message_complete = {
                        "topic_name": topic_name,
                        "content": info_message["message"]
                    }
                    await self.send_message(recipient=recipient, message=message_complete)

    async def send_updates(self) -> None:
        """
        Method to send updates of pending messages per user.
        :return: None
        """
        # Código para enviar actualizaciones a los usuarios suscritos
        pass


    async def run(self) -> None:
        """
        Method to run the WebSocketHandler.

        :return: None
        """
        async for message in self.websocket:
            print(f"Mensaje recibido: {message}")
            try:
                data = json.loads(message)
               
                action = data['action']

                if action == 'authenticate':
                    if 'token' not in data:
                        print("no se mando token..")

                    await self.authenticate(data['token'])
                elif action == 'subscribe':
                    channel = data['channel']
                    subscribed = await self.subscribe(channel=channel)
                    if subscribed:
                        # Si la suscripción fue exitosa, enviar un mensaje de confirmación al usuario.
                        await self.websocket.send(json.dumps({
                            "accion": "subscribe",
                            "canal": channel,
                            "resultado": "ok"
                        }))
                    else:
                        # Si la suscripción no fue exitosa, enviar un mensaje de error al usuario.
                        await self.websocket.send(json.dumps({
                            "accion": "subscribe",
                            "canal": channel,
                            "resultado": "error"
                        }))

                elif action == 'message':
                    print("entro action message")
                    info_message = {
                        "topic": data["topic_name"],
                        "message": data["content"]
                    }
                    print(f"info_message: {info_message}")
                    await self.handle_message(info_message)

                else:
                    # Acción no reconocida
                    pass
            except Exception:
                # Error al procesar el mensaje
                print(f"Error al procesar el mensaje: {traceback.format_exc()}")
        # Se cerró la conexión WebSocket
        await self.websocket.close()


# Lista de usuarios conectados y sus respectivos objetos WebSocketHandler
CONNECTED_USERS = {}
# Diccionario de mensajes pendientes para usuarios desconectados
PENDING_MESSAGES= {}
# Esta variable guarda la información de los canales a los que los usuarios pueden suscribirse.
# La clave es el nombre del canal y el valor es una lista de usuarios autorizados.
CHANNELS = {
    "public": {
        "usuarios": ["diego", "omar", "satoshi"],
        "topicos": ["noticias", "deportes"]
    },
    "private": {
        "usuarios": ["diego", "satoshi"],
        "topicos": ["trabajo"]
    }
}
# Función de servidor WebSocket para aceptar conexiones entrantes
async def websocket_server(websocket, path: str) -> None:
    """
    Function to accept incoming WebSocket connections and validate
    credentials if are correct.

    :param websocket: The WebSocket connection.
    :param path: The path of the WebSocket connection like url params.
    """
    websocket_handler = WebSocketHandler(websocket)
    access = await websocket_handler.authenticate(token=path[1:])
    if not access:
        await websocket.close()

    CONNECTED_USERS[websocket_handler.username] = websocket_handler
    # print(f"Connected users: {CONNECTED_USERS}")
    asyncio.create_task(websocket_handler.send_updates())
    await websocket_handler.run()
    if websocket_handler.username in CONNECTED_USERS:
        del CONNECTED_USERS[websocket_handler.username]

if __name__ == "__main__":
    # Configuración del servidor WebSocket
    print("Run server WS!")
    start_server = websockets.serve(websocket_server, "localhost", 5000)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()