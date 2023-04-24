try:
    import sys
    import jwt
    from datetime import datetime, timedelta
except ImportError as err_imp:
    print(f"The following import error occurred: {err_imp}")

# Definir la clave secreta para firmar el token
SECRET_KEY = "B7PwGjhYohg"

def encode_token(username: str, days:int=0, minutes:int=120, **kwargs) -> str:
    """
    Method to generate a token for a user with a given expiration time.

    :param username: Username of the user to generate the token for
    :param days: Amount of days that the token will be valid
    :param minutes: Amount of minutes that the token will be valid
    :param kwargs: Any other data to include in the token payload
    :return: The generated token
    """
    payload_core = {
        'exp': datetime.utcnow() + timedelta(days=days, minutes=minutes),
        'iat': datetime.utcnow(),
        'sub': username
    }
    if kwargs:
        payload_core.update(kwargs)


    return jwt.encode(payload_core, SECRET_KEY, algorithm="HS256")

if __name__ == "__main__":
    # Definir los datos a incluir en el payload del token (pueden ser cualquier datos que quieras incluir)
    payload = {
        "description": "Test token"
    }
    # get user from terminal
    if len(sys.argv) < 1:
        print("Please provide a username")
        sys.exit(1)
    else:
        user = sys.argv[1]
        token = encode_token(username=user, days=1, minutes=0, payload=payload)
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        print("\n"+token, end="\n\n")
        print(decoded_token)