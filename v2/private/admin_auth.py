import jwt
from configuration import ConfigurationVariables

def create_token(user_id, username):
    encoded_jwt = jwt.encode({"session_type": user_id, "username": username}, ConfigurationVariables.JWT_SECRET, algorithm="HS256")
    return encoded_jwt

def is_authorized(token):
    try:
        admin = jwt.decode(token, ConfigurationVariables.JWT_SECRET, algorithms=["HS256"])
        if admin["session_type"] == "Administrator":
            return True
    except:
        return False
    return False