try:
    from app import app
    from http import HTTPStatus
    from flask import Response, request, jsonify, make_response
    from utils import (get_topics,create_topic,update_topic,delete_topic,
                       create_message,get_messages,update_messages,
                       encode_token, decode_token,
                       get_users, create_user)
except ImportError as e_imp:
    print(f"The following import ERROR occurred in {__file__}: {e_imp}")

# -------------Endpoints-------------
@app.route("/api/v1/topics", methods=["GET", "POST", "PUT", "DELETE"])
def topics_actions() -> Response:
    """
    This function handles the endpoints for the topics.
    """
    if request.method == "GET":
        # get parameters from the request
        user = request.args.get("user")
        topic_name = request.args.get("topic_name")
        topics = get_topics(user, topic_name)
        if isinstance(topics, dict):
            return make_response(jsonify(topics), HTTPStatus.OK)
        elif isinstance(topics, list):
            resp = {
                "topics": topics
            }
            return make_response(jsonify(resp), HTTPStatus.OK)
        else:
            return make_response(jsonify({"message": "No topics found"}), HTTPStatus.NOT_FOUND)
        
    elif request.method == "POST":
        body:dict[str,str] = request.get_json()
        if isinstance(body, dict):
            result = create_topic(**body)
            if result:
                return make_response(jsonify({"message": "Topic created"}), HTTPStatus.CREATED)
            else:
                return make_response(jsonify({"message": "Topic not created"}), HTTPStatus.BAD_REQUEST)
            
    elif request.method == "PUT":
        #  to update members of a topic, for subscribe
        body:dict[str,str] = request.get_json()
        if isinstance(body, dict):
            result = update_topic(**body)
            if result:
                return make_response(jsonify({"message": "User subscribed"}), HTTPStatus.OK)
            else:
                return make_response(jsonify({"message": "User not subscribed"}), HTTPStatus.BAD_REQUEST)
            
    elif request.method == "DELETE":
        # to delete a topic
        body:dict[str,str] = request.get_json()

        if isinstance(body, dict):
            result = delete_topic(**body)
            if result:
                return make_response(jsonify({"message": "Topic deleted"}), HTTPStatus.OK)
            else:
                return make_response(jsonify({"message": "Topic not deleted"}), HTTPStatus.BAD_REQUEST)
            
@app.route("/api/v1/messages", methods=["GET", "POST", "PUT"])
def messages_queues() -> Response:
    """
    This function handles the endpoints for the messages queue from pending_messages.json.
    """
    if request.method == "GET":
        # get parameters from the request
        user = request.args.get("user")
        messages = get_messages(user)
        if len(messages) < 0:
            return make_response(jsonify({"message": "No messages found"}), HTTPStatus.NOT_FOUND)
        resp = {
            "messages": messages
        }
        return make_response(jsonify(resp), HTTPStatus.OK)
    
    elif request.method == "POST":
        body:dict[str,str] = request.get_json()
        if isinstance(body, dict):
            result = create_message(body)
            if result:
                return make_response(jsonify({"message": "Message created"}), HTTPStatus.CREATED)
            else:
                return make_response(jsonify({"message": "Message not created"}), HTTPStatus.BAD_REQUEST)
            
    elif request.method == "PUT":
        # to delete a message
        body:dict[str,str] = request.get_json()
        if isinstance(body, dict):
            messages = body["messages"]
            result = update_messages(messages, body["user"])
            if result:
                return make_response(jsonify({"message": "Message deleted"}), HTTPStatus.OK)
            else:
                return make_response(jsonify({"message": "Message not deleted"}), HTTPStatus.BAD_REQUEST)
            
@app.route("/api/v1/token", methods=["GET"])
def token() -> Response:
    # Validates if Action header exists
    if "Action" not in request.headers:
        return make_response(jsonify({"message": "Action header not found"}), HTTPStatus.BAD_REQUEST)
    else:
        action = request.headers["Action"]
        if action == "encode":
            # get query params in dictionary
            params = request.args.to_dict()
            user = params.pop("user")
            token = encode_token(username=user, days=1, minutes=0, payload=params)
            if token:
                return make_response(jsonify({"token": token}), HTTPStatus.OK)
            else:
                return make_response(jsonify({"message": "Token not generated"}), HTTPStatus.BAD_REQUEST)
        elif action == "decode":
            # get token from params
            decoded_token = request.args.get("token")
            decoded_token = decode_token(decoded_token)
            if isinstance(decoded_token, dict):
                return make_response(jsonify(decoded_token), HTTPStatus.OK)
            else:
                return make_response(jsonify({"message": "Token not decoded"}), HTTPStatus.BAD_REQUEST)
    
@app.route("/api/v1/users", methods=["GET", "POST"])
def users_actions() -> Response:
    """
    This function handles the endpoints for the users.
    """
    if request.method == "GET":
        resp = get_users()
        if isinstance(resp, list):
            return make_response(jsonify(resp), HTTPStatus.OK)
        else:
            return make_response(jsonify({"message": "No users found"}), HTTPStatus.NOT_FOUND)
        
    elif request.method == "POST":
        body:dict[str,str] = request.get_json()
        body["new_user"] = body.pop("user")
        if isinstance(body, dict):
            result = create_user(**body)
            if result:
                return make_response(jsonify({"message": "User created"}), HTTPStatus.CREATED)
            else:
                return make_response(jsonify({"message": "User not created"}), HTTPStatus.BAD_REQUEST)