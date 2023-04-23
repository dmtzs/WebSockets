try:
    import jwt
    import json
    import asyncio
    import requests
    import traceback
    import websockets
except ImportError as err_imp:
    print(f"The following import error occurred: {err_imp}")

# Definir una clase para manejar las conexiones WebSocket
class WebSocketHandler:
    def __init__(self, websocket):
        self.websocket = websocket
        self.username = None
        self.heartbeat_task = None

    async def send_heartbeat(self):
        try:
            await self.websocket.send(json.dumps({
                "action": "heartbeat"
            }))
        except Exception as err:
            print(f"Error sending heartbeat: {err}")
            await self.websocket.close()

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
                message_to_send = json.dumps(message)
                await recipient_socket.websocket.send(message_to_send)
                print(f"Message sent to destinatary: {recipient}: {message_to_send}")
        else:
            print(f"Destinatary {recipient} not connected, message stored to be delivered later.")
            URL = "http://localhost:5001/api/v1/messages"
            BODY = message
            BODY |= {"user": self.username}
            response = requests.post(url=URL, json=BODY)
            if response.status_code == 200:
                print(f"Message stored in database: {message}")
            else:
                print(f"Message not stored in database, contact devs to solve: {message}")

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

    async def subscribe(self, topic_name:str) -> bool:
        """
        Method to subscribe the user to a public topic.

        :param topic_name: The topic name that user wants to subscribe.
        :return: True if the user was subscribed, False otherwise.
        """
        URL = "http://localhost:5001/api/v1/topics"
        PARAMS = {"topic_name": topic_name, "user": self.username}
        try:
            response = requests.put(url=URL, params=PARAMS)
            if response.status_code == 200:
                return True
            return False
        except Exception:
            print(f"Error in subscribe: {traceback.format_exc()}")
            return False
    
    async def create_topic(self, topic_name:str, is_private:bool=False) -> bool:
        """
        Method to create a new topic.

        :param topic_name: The topic name.
        :return: True if the topic was created, False otherwise.
        """
        URL = "http://localhost:5001/api/v1/topics"
        BODY = {
            "topic_name": topic_name,
            "user": self.username,
            "is_private": is_private
        }
        try:
            response = requests.post(url=URL, json=BODY)
            if response.status_code == 201:
                return True
            return False
        except Exception:
            print(f"Error in create_topic: {traceback.format_exc()}")
            return False
        
    async def get_topic(self, topic_name:str) -> dict[str, str|bool]|None:
        """
        Method to get the topic information.

        :param topic_name: The topic name.
        :return: A dictionary with the topic information.
        """
        URL = "http://localhost:5001/api/v1/topics"
        PARAMS = {"topic_name": topic_name}
        try:
            response = requests.get(url=URL, params=PARAMS)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception:
            print(f"Error in get_topic: {traceback.format_exc()}")
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
                                        "message": "You are not a member of this topic but you can subscribe to this topic cause is public"
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
        URL = "http://localhost:5001/api/v1/messages"
        PARAMS = {"user": self.username}
        try:
            response = requests.get(url=URL, params=PARAMS)
            if response.status_code == 200:
                pending_messages = response.json()
                body_update = pending_messages
                if len(pending_messages) > 0:
                    for message in pending_messages["messages"]:
                        del message["not_delivered_to_user_id_topic"]
                        await self.send_message(recipient=self.username, message=message)
                body_update |= {"user": self.username}
                response = requests.put(url=URL, json=body_update)
                if response.status_code == 200:
                    print("Messages updated")
                else:
                    print("Error updating messages")
        except Exception:
            print(f"Error in send_updates: {traceback.format_exc()}")

    async def run(self) -> None:
        """
        Method to run the WebSocketHandler.

        :return: None
        """
        self.heartbeat_task = asyncio.create_task(self.send_heartbeat())
        while True:
            try:
                message = await asyncio.wait_for(self.websocket.recv(), timeout=30)# in seconds the timeout
                print(f"Message received: {message}")
                data=None
                try:
                    data:dict[str,any] = json.loads(message)
                except Exception:
                    print(f"data sent from {self.username} is not a json")
                finally:
                    if data is not None:
                        action = data.get("action")
                        if action == "subscribe":
                            topic_name = data['topic_name']
                            subscribed = await self.subscribe(topic_name=topic_name)
                            if subscribed:
                                # Si la suscripción fue exitosa, enviar un mensaje de confirmación al usuario.
                                await self.websocket.send(json.dumps({
                                    "action": "subscribe",
                                    "topic_name": topic_name,
                                    "result": "ok"
                                }))
                            else:
                                # Si la suscripción no fue exitosa, enviar un mensaje de error al usuario.
                                await self.websocket.send(json.dumps({
                                    "action": "subscribe",
                                    "topic_name": topic_name,
                                    "result": "error"
                                }))

                        elif action == "create":
                            topic_name = data["topic_name"]
                            # Create the topic
                            created = await self.create_topic(topic_name=topic_name, is_private=data["is_private"])
                            if created:
                                # If the topic was created, send a confirmation message to the user.
                                await self.websocket.send(json.dumps({
                                    "action": "create",
                                    "topic_name": topic_name,
                                    "result": "ok"
                                }))
                            else:
                                # If the topic was not created, send an error message to the user.
                                await self.websocket.send(json.dumps({
                                    "action": "create",
                                    "topic_name": topic_name,
                                    "result": "error"
                                }))

                        elif action == "message":
                            info_message = {
                                "topic": data["topic_name"],
                                "message": data["content"]
                            }
                            await self.handle_message(info_message)

                        elif action == "disconnect":
                            break

                        else:
                            # Unknown action
                            info_message = {
                                "topic": "error",
                                "message": "Unknown action received",
                                "action": action
                            }
                            await self.handle_message(info_message)
                    else:
                        # No action
                        info_message = {
                            "topic": "error",
                            "message": "No action received"
                        }
                        await self.handle_message(info_message)
            except asyncio.TimeoutError:
                # Send a heartbeat to check if the connection is still alive
                self.heartbeat_task = asyncio.create_task(self.send_heartbeat())
            except websockets.exceptions.ConnectionClosedOK:
                # Connection closed by the client
                del CONNECTED_USERS[self.username]
                print(f"Connection closed for user {self.username}")
                break
            except Exception as err:
                # Error at processing the message
                print(f"Error at processing the message: {traceback.format_exc()}")
                info_message = {
                    "topic": "error",
                    "message": "Error at processing the message, contact technical support",
                    "error": str(err)
                }
                await self.handle_message(info_message)

        # Close the websocket connection and cancel the heartbeat task
        self.heartbeat_task.cancel()
        await self.websocket.close()

CONNECTED_USERS = {} # Dictionary to store connected users.

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