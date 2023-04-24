try:
    import json
except ImportError as e_imp:
    print(f"The following import ERROR occurred in {__file__}: {e_imp}")

def get_topics(user:str|None=None,topic_name:str|None=None) -> list[dict[str, list[str]|str|bool]] | dict[str, list[str]|str|bool]:
    """
    Returns a list of topics or a single topic if a topic name is provided.
    If a user is provided, it will return a list of topics that the user is a member of.

    :param user: The user to search for
    :type user: str
    :param topic_name: The topic name to search for
    :type topic_name: str
    :return: A list of topics or a single topic
    """
    try:
        with open("topics.json", "r") as file:
            topics:list[dict[str, list[str]|str|bool]] = json.load(file)
        if user is not None:
            user_topics = []
            for per_topic in topics["topics"]:
                if user in per_topic["members"]:
                    user_topics.append(per_topic)
            return user_topics
        elif topic_name is not None:
            for per_topic in topics["topics"]:
                if per_topic["topic_name"] == topic_name:
                    return per_topic
    except FileNotFoundError as e_f:
        print(f"The following FILE ERROR occurred in {__file__}: {e_f}")
        return []
    except json.decoder.JSONDecodeError as e_j:
        print(f"The following JSON ERROR occurred in {__file__}: {e_j}")
        return []

def create_topic(topic_name:str,user:str,is_private:bool=False) -> bool:
    """
    Creates a new topic

    :param topic_name: The topic name to search for
    :type topic_name: str
    :param user: The user to add to the topic
    :type user: str
    :param is_private: A boolean indicating if the topic is private
    :type is_private: bool
    :return: A boolean indicating if the topic was created
    """
    try:
        with open("topics.json", "r") as file:
            topics:list[dict[str, list[str]|str|bool]] = json.load(file)
        new_register = {
            "topic_name": topic_name,
            "creator": user,
            "is_user": False,
            "members": [user],
            "is_private": is_private
        }
        topics["topics"].append(new_register)
        with open("topics.json", "w") as file:
            json.dump(topics, file, indent=4)
        return True
    except FileNotFoundError as e_f:
        print(f"The following FILE ERROR occurred in {__file__}: {e_f}")
    except json.decoder.JSONDecodeError as e_j:
        print(f"The following JSON ERROR occurred in {__file__}: {e_j}")
    return False

def update_topic(topic_name:str,user:str,user_source:str|None=None) -> bool:
    """
    Updates the members of a topic, for subscribe

    :param topic_name: The topic name to search for
    :type topic_name: str
    :param user: The user to add to the topic
    :type user: str
    :return: A boolean indicating if the topic was updated
    """
    try:
        with open("topics.json", "r") as file:
            topics:list[dict[str,list[str]|str|bool]] = json.load(file)
        for per_topic in topics["topics"]:
            if per_topic["topic_name"] == topic_name:
                if not per_topic["is_private"] and user not in per_topic["members"]:
                    per_topic["members"].append(user)
                    with open("topics.json", "w") as file:
                        json.dump(topics, file, indent=4)
                    return True
                if (per_topic["is_private"]) and (user not in per_topic["members"]):
                    if user_source is not None and user_source in per_topic["members"]:
                        per_topic["members"].append(user)
                        with open("topics.json", "w") as file:
                            json.dump(topics, file, indent=4)
                        return True
                    else:
                        print("user source is None")
                else:
                    print("user already in topic or something else happen")
            else:
                print("topic not found")
        return False
    except FileNotFoundError as e_f:
        print(f"The following FILE ERROR occurred in {__file__}: {e_f}")
        return False
    except json.decoder.JSONDecodeError as e_j:
        print(f"The following JSON ERROR occurred in {__file__}: {e_j}")
        return False

def delete_topic(topic_name:str) -> bool:
    """
    Deletes a topic

    :param topic_name: The topic name to search for
    :type topic_name: str
    :return: A boolean indicating if the topic was deleted
    """
    try:
        with open("topics.json", "r") as file:
            topics:list[dict[str, list[str]|str|bool]] = json.load(file)
        for per_topic in topics:
            if per_topic["topic_name"] == topic_name:
                topics.remove(per_topic)
                with open("topics.json", "w") as file:
                    json.dump(topics, file, indent=4)
                return True
    except FileNotFoundError as e_f:
        print(f"The following FILE ERROR occurred in {__file__}: {e_f}")
    except json.decoder.JSONDecodeError as e_j:
        print(f"The following JSON ERROR occurred in {__file__}: {e_j}")
    return False

def create_message(body:dict[str,str]) -> bool:
    """
    Creates a new pending messages
    """
    try:
        with open("pending_messages.json", "r") as file:
            messages:list[dict[str, list[str]|str|bool]] = json.load(file)
        new_register = {
            "topic_name": body["topic_name"],
            "action": "message",
            "content": body["content"],
            "not_delivered_to_user_id_topic": [body["user"]]
        }
        # validate if the message already exists using content and topic_name
        control_register = False
        for per_message in messages["messages"]:
            if per_message["content"] == new_register["content"] and per_message["topic_name"] == new_register["topic_name"]:
                if body["user"] not in per_message["not_delivered_to_user_id_topic"]:
                    per_message["not_delivered_to_user_id_topic"].append(body["user"])
                    control_register = True
        if not control_register:
            messages["messages"].append(new_register)
        with open("pending_messages.json", "w") as file:
            json.dump(messages, file, indent=4)
        return True
    except FileNotFoundError as e_f:
        print(f"The following FILE ERROR occurred in {__file__}: {e_f}")
        return False
    except json.decoder.JSONDecodeError as e_j:
        print(f"The following JSON ERROR occurred in {__file__}: {e_j}")
        return False

def get_messages(user:str):
    """
    Gets the pending messages by user

    :param user: The user to search for
    :type user: str
    :return: A list of messages that the user has pending
    """
    try:
        with open("pending_messages.json", "r") as file:
            messages:list[dict[str, list[str]|str|bool]] = json.load(file)
        user_messages = []
        for per_message in messages["messages"]:
            if user in per_message["not_delivered_to_user_id_topic"]:
                user_messages.append(per_message)
        return user_messages
    except FileNotFoundError as e_f:
        print(f"The following FILE ERROR occurred in {__file__}: {e_f}")
        return []
    except json.decoder.JSONDecodeError as e_j:
        print(f"The following JSON ERROR occurred in {__file__}: {e_j}")
        return []
    
def update_messages(messages:list[dict[str, list[str]|str|bool]], user:str) -> bool:
    """
    Updates the pending messages

    :param messages: The messages to update
    :type messages: list[dict[str, list[str]|str|bool]]
    """
    try:
        with open("pending_messages.json", "r") as file:
            messages_db:list[dict[str, list[str]|str|bool]] = json.load(file)
        # validates if the message already exists using content and topic_name and updates the not_delivered_to_user_id_topic deleting the user
        for per_message in messages_db["messages"]:
            for per_message_to_update in messages:
                if per_message["content"] == per_message_to_update["content"] and per_message["topic_name"] == per_message_to_update["topic_name"]:
                    if user in per_message["not_delivered_to_user_id_topic"]:
                        per_message["not_delivered_to_user_id_topic"].remove(user)
        with open("pending_messages.json", "w") as file:
            json.dump(messages_db, file, indent=4)
        return True
    except FileNotFoundError as e_f:
        print(f"The following FILE ERROR occurred in {__file__}: {e_f}")
        return False
    except json.decoder.JSONDecodeError as e_j:
        print(f"The following JSON ERROR occurred in {__file__}: {e_j}")
        return False