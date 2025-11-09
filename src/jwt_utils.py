import jwt
import datetime

SECRET_KEY = "very-very-seret-key"


def create_jwt_token(token_payload: dict):
    expiration_time = datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)
    token_payload["exp"] = expiration_time
    token = jwt.encode(
        payload=token_payload,
        algorithm="HS256",
        key=SECRET_KEY
    )
    return token


def decode_jwt_token(token: str):
    jwt_data = jwt.decode(
        jwt=token,
        algorithms="HS256",
        key=SECRET_KEY
    )
    return jwt_data

def main():
    token = create_jwt_token({"name": "Misha"})
    print(f"JWT token: {token}")
    payload = decode_jwt_token(token)
    print(f"Payload: {payload}")


if __name__ == "__main__":
    main()