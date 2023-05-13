import json
import unittest
from app import app

class FlaskAppTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_get_topics(self):
        response = self.app.get("/api/v1/topics?topic_name=gdcode")
        self.assertEqual(response.status_code, 200)

    def test_create_topic(self):
        data = {
            "topic_name": "test_topic",
            "user": "diego",
            "is_private": True
        }
        headers = {
            "Content-Type": "application/json"
        }
        response = self.app.post("/api/v1/topics",
                                 headers=headers,
                                 data=json.dumps(data))
        self.assertEqual(response.status_code, 201)

    def test_update_topic_members(self):
        data = {
            "topic_name": "gdcode",
            "user": "eder",
            "user_source": "diego"
        }
        headers = {
            "Content-Type": "application/json"
        }
        response = self.app.put("/api/v1/topics",
                                headers=headers,
                                data=json.dumps(data))
        self.assertEqual(response.status_code, 200)

    def test_delete_topic(self):
        data = {
            "topic_name": "test_topic"
        }
        headers = {
            "Content-Type": "application/json"
        }
        response = self.app.delete("/api/v1/topics",
                                   headers=headers,
                                   data=json.dumps(data))
        self.assertEqual(response.status_code, 200)

    def test_get_messages(self):
        response = self.app.get("/api/v1/messages?user=diego")
        self.assertEqual(response.status_code, 200)
    
    def test_get_messages_no_params(self):
        response = self.app.get("/api/v1/messages")
        self.assertEqual(response.status_code, 200)

    def test_create_message(self):
        data = {
            "user": "diego",
            "topic_name": "test_create_message",
            "content": "test_message_unittest"
        }
        headers = {
            "Content-Type": "application/json"
        }
        response = self.app.post("/api/v1/messages",
                                 headers=headers,
                                 data=json.dumps(data))
        self.assertEqual(response.status_code, 201)

    def test_update_messages(self):
        data = {
            "messages": [
                {
                    "action": "message",
                    "content": "Content of the message 1",
                    "topic_name": "general"
                },
                {
                    "action": "message",
                    "content": "Content of the message 2",
                    "topic_name": "noticias"
                },
                {
                    "action": "message",
                    "content": "Content of the message 3",
                    "topic_name": "noticias"
                }
            ],
            "user": "omar"
        }
        headers = {
            "Content-Type": "application/json"
        }
        response = self.app.put("/api/v1/messages",
                                headers=headers,
                                data=json.dumps(data))
        self.assertEqual(response.status_code, 200)

    def test_get_users(self):
        response = self.app.get("/api/v1/users")
        self.assertEqual(response.status_code, 200)

    def test_create_user(self):
        data = {
            "user": "test_user"
        }
        headers = {
            "Content-Type": "application/json"
        }
        response = self.app.post("/api/v1/users",
                                 headers=headers,
                                 data=json.dumps(data))
        self.assertEqual(response.status_code, 201)

    def test_token(self):
        response = self.app.get("/api/v1/token?user=test_user")
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()