from flask import Blueprint, request
from .actions import private_users_list, private_list_tasks, private_login, generate_uuid, create_private_task, private_create_user, private_document_add, private_delete_task, private_delete_user, private_user_reset, private_document_delete


# Defining a blueprint
private = Blueprint(
    'private', __name__
)

@private.route('/api/v2/private/login', methods=["POST"])
def api_private_login():
    post_data = request.json
    try:
        username = post_data["username"]
        password = post_data["password"]
    except:
        return {"result":"failed","message":"Username and password combination required."}
    
    return private_login(username, password)

@private.route('/api/v2/private/user/create', methods=["POST"])
def api_private_user_create():
    user_data = request.json
    try:
        token = request.headers.get("Authorization")
    except:
        return {"result":"failed", "message":"Missing authorization header."}, 403
    
    try:
        username = user_data["username"]
        age = user_data["age"]
        full_name = user_data["full_name"]
        user_uuid = generate_uuid()
    except:
        return {"result":"failed", "message":"Insufficient parameters provided."}, 400
    return private_create_user(user_uuid, full_name, username, age, token)

@private.route('/api/v2/private/user/reset', methods=["PATCH"])
def api_private_user_reset():
    try:
        new_password = request.json["new_password"]
        user_uuid = request.json["user_uuid"]
    except:
        return {"result":"failed", "message":"Insufficient parameters provided."}, 400
    
    return private_user_reset(new_password, user_uuid)

@private.route('/api/v2/private/task/create', methods=["POST"])
def api_private_task_create():
    task_data = request.json
    try:
        token = request.headers.get("Authorization")
    except:
        return {"result":"failed", "message":"Missing authorization header."}, 403
    
    try:
        task_title = task_data["task_title"]
        task_details = task_data["task_details"]
        task_uuid = generate_uuid()
        assigned_user = task_data["assigned_user"]
    except:
        return {"status":"failed", "message":"Insufficient parameters provided."}, 400
    
    return create_private_task(task_title, task_details, assigned_user, token)

@private.route('/api/v2/private/task/<task_uuid>', methods=["DELETE"])
def api_private_task_delete(task_uuid):
    try:
        token = request.headers.get("Authorization")
    except:
        return {"result":"failed", "message":"Missing authorization header."}, 403
    
    return private_delete_task(task_uuid, token)

@private.route('/api/v2/private/tasks/list', methods=["GET"])
def api_private_task_list():
    try:
        token = request.headers.get("Authorization")
    except:
        return {"result":"failed", "message":"Missing authorization header."}, 403
    
    return private_list_tasks(token)

@private.route('/api/v2/private/user/<user_uuid>', methods=["DELETE"])
def api_private_user_delete(user_uuid):
    try:
        token = request.headers.get("Authorization")
    except:
        return {"result":"failed", "message":"Missing authorization header."}, 403
    
    return private_delete_user(user_uuid, token)

@private.route('/api/v2/private/users/list', methods=["GET"])
def api_private_users_list():
    try:
        token = request.headers.get("Authorization")
    except:
        return {"result":"failed", "message":"Missing authorization header."}, 403
    
    return private_users_list(request.args.get("search"), token)

@private.route('/api/v2/private/document/add', methods=["POST"])
def api_private_document_add():
    document_data = request.json
    try:
        token = request.headers.get("Authorization")
    except:
        return {"result":"failed", "message":"Missing authorization header."}, 403
    
    try:
        document = document_data["document_name"]
    except:
        return {"status":"failed", "message":"Insufficient parameters provided."}, 400
    
    return private_document_add(document, token)

@private.route('/api/v2/private/document/<document_uuid>', methods=["DELETE"])
def api_private_document_delete(document_uuid):
    try:
        token = request.headers.get("Authorization")
    except:
        return {"result":"failed", "message":"Missing authorization header."}, 403
        
    return private_document_delete(document_uuid, token)
    

    
