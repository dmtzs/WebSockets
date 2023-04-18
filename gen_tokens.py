import jwt
from datetime import datetime, timedelta

# Definir la clave secreta para firmar el token
secret_key = "B7PwGjhYohg"

def encode_token(username: str, days:int=0, minutes:int=120, **kwargs) -> dict[str, str]:
    """
    Método para crear un JWT por defecto vence en 5min.

    :param username: Nombre de usuario
    :param days: Cantidad de días que el token será válido
    :param minutes: Cantidad de minutos que el token será válido
    :param kwargs: Cualquier otro dato que quieras incluir en el payload del token
    """
    payload = {
        'exp': datetime.utcnow() + timedelta(days=days, minutes=minutes),
        'iat': datetime.utcnow(),
        'sub': username
    }
    if kwargs:
        payload.update(kwargs)


    return jwt.encode( payload, secret_key, algorithm="HS256")

if __name__ == "__main__":
    # Definir los datos a incluir en el payload del token (pueden ser cualquier datos que quieras incluir)
    payload = {
        "descripcion": "cualquier_cosa"
    }

    token = encode_token(username='satoshi', days=1, minutes=0, payload=payload)
    print(token)