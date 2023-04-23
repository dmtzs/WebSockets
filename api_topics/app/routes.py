try:
    from app import app
    from http import HTTPStatus
    from flask import Response, request, jsonify, make_response
    from utils import get_topics, create_topic, update_topic, delete_topic, create_message, get_messages, update_messages
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
            result = create_message(**body)
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