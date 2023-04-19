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
            if isinstance(message, dict):
                message = json.dumps(message)
            await recipient_socket.websocket.send(message)
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
            return True
        except:
            # Si el token no es válido.
            print("Invalid token")
            return False

    async def subscribe(self, channel):# TODO: Still in development
        """Función para suscribirse a un canal o tema.  """
        # Verificar que el canal exista y el usuario tenga permiso para suscribirse.
        if channel in CHANNELS and self.username in CHANNELS[channel]:
            # Agregar al usuario a la lista de usuarios suscritos a este canal.
            CHANNELS[channel].append(self.username)
            return True
        else:
            return False
        
    async def get_topic(self, topic_name:str) -> dict[str, str|bool]|None:
        """
        Method to get the topic information.

        :param topic_name: The topic name.
        :return: A dictionary with the topic information.
        """
        with open("topics.json", "r") as file:
            topic_info = json.load(file)
        for topic in topic_info["topics"]:
            if topic["topic_name"] == topic_name:
                return topic
        return None

    async def handle_message(self, info_message:dict|None=None) -> None:
        """
        Method to handle incoming messages and be sent to the correct destinataries.

        :param info_message: The message to be sent.
        :return: None
        """
        try:
            if info_message is not None:
                topic_name = info_message["topic"]
                if topic_name == "error":
                    # Send the error message to the user that sent the error.
                    await self.send_message(recipient=self.username, message=info_message)
                else:
                    topic_info = await self.get_topic(topic_name)
                    if topic_info is not None:
                        if not topic_info["is_user"]:
                            if self.username in topic_info["members"]:
                                for recipient in topic_info["members"]:
                                    message_complete = {
                                        "topic_name": topic_name,
                                        "content": info_message["message"]
                                    }
                                    await self.send_message(recipient=recipient, message=message_complete)
                            else:
                                # Send the error message to the user that sent the error.
                                if not topic_info["is_private"]:
                                    info_message = {
                                        "topic": "error",
                                        "topic_name": topic_name,
                                        "message": "You are not a member of this topic but you can suscribe to this topic cause is public"
                                    }
                                else:
                                    info_message = {
                                        "topic": "error",
                                        "topic_name": topic_name,
                                        "message": "You are not a member of this topic, you need to request access to owner cause is private"
                                    }
                                await self.send_message(recipient=self.username, message=info_message)
                        else:
                            message_complete = {
                                "user_source": self.username,
                                "content": info_message["message"]
                            }
                            await self.send_message(recipient=topic_name, message=message_complete)
                    else:
                        # Send the error message to the user that sent the error.
                        info_message = {
                            "topic": "error",
                            "topic_name": topic_name,
                            "message": "Topic not found"
                        }
                        await self.send_message(recipient=self.username, message=info_message)
            else:
                print("No message received")
                
        except Exception as err:
            print(f"Error in handle_message: {traceback.format_exc()}")
            # Send the error message to the user that sent the error.
            info_message = {
                "topic": "error",
                "message": "Error in handle_message, contact the administrator",
                "error": str(err)
            }
            await self.send_message(recipient=self.username, message=info_message)

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
            print(f"Message received: {message}")
            try:
                data = json.loads(message)
                action = data['action']

                if action == 'subscribe':
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
                    info_message = {
                        "topic": data["topic_name"],
                        "message": data["content"]
                    }
                    await self.handle_message(info_message)

                else:
                    # Unknown action
                    info_message = {
                        "topic": "error",
                        "message": "Unknown action received",
                        "action": action
                    }
            except Exception as err:
                # Error at processing the message
                print(f"Error at processing the message: {traceback.format_exc()}")
                info_message = {
                    "topic": "error",
                    "message": "Error at processing the message, contact technical support",
                    "error": str(err)
                }
                await self.handle_message(info_message)
        # Close the websocket connection
        await self.websocket.close()


CONNECTED_USERS = {} # Dictionary to store connected users.
PENDING_MESSAGES= {}
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
    # TODO: Verify if there are pending messages.
    asyncio.create_task(websocket_handler.send_updates())
    await websocket_handler.run()
    if websocket_handler.username in CONNECTED_USERS:
        del CONNECTED_USERS[websocket_handler.username]

if __name__ == "__main__":
    # Code to run the WebSocket server
    print("Run server WS!")
    start_server = websockets.serve(websocket_server, "localhost", 5000)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()