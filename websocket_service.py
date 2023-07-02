try:
    import os
    import asyncio
    import websockets
    from dotenv import load_dotenv
    from websocket_library import WebSocketHandler
except ImportError as err_imp:
    print(f"The following import error occurred: {err_imp}")


# CONNECTED_USERS = {} # Dictionary to store connected users.

async def websocket_server(websocket, path: str) -> None:
    """
    Function to accept incoming WebSocket connections and validate
    credentials if are correct.

    Args:
        websocket: WebSocket connection.
        path(str): Path of the WebSocket connection.

    Returns:
        None
    """
    websocket_handler = WebSocketHandler(websocket)
    access = await websocket_handler.authenticate(token=path[1:])
    if not access:
        await websocket.close()
    websocket_handler.CONNECTED_USERS[websocket_handler.username] = websocket_handler
    asyncio.create_task(websocket_handler.send_updates())
    await websocket_handler.run()
    if websocket_handler.username in websocket_handler.CONNECTED_USERS:
        del websocket_handler.CONNECTED_USERS[websocket_handler.username]

if __name__ == "__main__":
    # Code to run the WebSocket server and loop
    print("Run server WS!")
    if os.path.exists("env_vars.env"):
        dotenv_path = os.path.join(os.path.dirname(__file__), "env_vars.env")
        load_dotenv(dotenv_path)
        print("Local environment variables loaded")
    else:
        print("Local environment variables not found, using the system environment variables")
    start_server = websockets.serve(websocket_server, "localhost", 5000)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()