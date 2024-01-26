import jwt
from configuration import ConfigurationVariables

def create_token(user_id, username):
    encoded_jwt = jwt.encode({"user_uuid": user_id, "username": username}, ConfigurationVariables.JWT_SECRET, algorithm="HS256")
    return encoded_jwt

def is_authorized(token):
    try:
        jwt.decode(token, ConfigurationVariables.JWT_SECRET, algorithms=["HS256"])
        return True
    except:
        return False
    
def authorization_info(token):
    return jwt.decode(token, ConfigurationVariables.JWT_SECRET, algorithms=["HS256"])