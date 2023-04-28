import jwt
import asyncio
import unittest
from unittest.mock import MagicMock, patch
from websocket_service import WebSocketHandler


class TestWebSocketHandler(unittest.TestCase):
    def setUp(self):
        self.websocket_mock = MagicMock()
        self.websocket_handler = WebSocketHandler(self.websocket_mock)

    def test_send_heartbeat(self):
        self.websocket_mock.send.side_effect = Exception("Error sending heartbeat")
        self.websocket_mock.close.return_value = asyncio.Future()
        self.websocket_mock.close.return_value.set_result(None)

        asyncio.run(self.websocket_handler.send_heartbeat())

        self.websocket_mock.send.assert_called_once_with('{"action": "heartbeat"}')
        self.websocket_mock.close.assert_called_once()

    def test_send_message(self):
        CONNECTED_USERS = {
            "user1": MagicMock(),
            "user2": MagicMock()
        }
        self.websocket_handler.CONNECTED_USERS = CONNECTED_USERS

        asyncio.run(self.websocket_handler.send_message("user1", {"content": "Hello"}))
        CONNECTED_USERS["user1"].websocket.send.assert_called_once_with('{"content": "Hello"}')

        asyncio.run(self.websocket_handler.send_message("user2", {"content": "Hi"}))
        CONNECTED_USERS["user2"].websocket.send.assert_called_once_with('{"content": "Hi"}')

        with self.assertRaises(KeyError):
            asyncio.run(self.websocket_handler.send_message("user3", {"content": "Hi"}))

    def test_authenticate(self):
        valid_token = jwt.encode({"sub": "user1"}, "B7PwGjhYohg", algorithm="HS256")
        invalid_token = "invalid_token"

        result = asyncio.run(self.websocket_handler.authenticate(valid_token))
        self.assertTrue(result)
        self.assertEqual(self.websocket_handler.username, "user1")
        self.assertEqual(self.websocket_handler.CONNECTED_USERS["user1"], self.websocket_mock)

        result = asyncio.run(self.websocket_handler.authenticate(invalid_token))
        self.assertFalse(result)
        self.assertIsNone(self.websocket_handler.username)
        self.assertNotIn("user1", self.websocket_handler.CONNECTED_USERS)

    def test_subscribe(self):
        with patch("requests.put") as put_mock:
            put_mock.return_value.status_code = 200

            result = asyncio.run(self.websocket_handler.subscribe("topic1"))
            self.assertTrue(result)
            put_mock.assert_called_once_with("http://localhost:5001/api/v1/topics", json={
                "topic_name": "topic1",
                "user": self.websocket_handler.username
            })

        with patch("requests.put") as put_mock:
            put_mock.return_value.status_code = 500

            result = asyncio.run(self.websocket_handler.subscribe("topic1"))
            self.assertFalse(result)
            put_mock.assert_called_once_with("http://localhost:5001/api/v1/topics", json={
                "topic_name": "topic1",
                "user": self.websocket_handler.username
            })


# Ejecuta las pruebas
if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestWebSocketHandler)
    unittest.TextTestRunner(verbosity=2).run(suite)