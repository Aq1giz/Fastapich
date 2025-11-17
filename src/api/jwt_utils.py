import jwt
import datetime

SECRET_KEY = "very-very-seret-key"


def create_jwt_token(
    token_payload: dict,
    algorithm: str= "HS256",
    key: str = SECRET_KEY    
):
    token = jwt.encode(
        payload=token_payload,
        algorithm=algorithm,
        key=key,
    )
    return token


def decode_jwt_token(
    token: str | bytes,
    algorithms=["HS256"],
    key=SECRET_KEY
):
    jwt_data = jwt.decode(
        jwt=token,
        algorithms=algorithms,
        key=key,
    )
    return jwt_data

def main():
    token = create_jwt_token({"name": "Misha"})
    print(f"JWT token: {token}")
    payload = decode_jwt_token(token)
    print(f"Payload: {payload}")


if __name__ == "__main__":
    main()