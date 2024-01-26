from flask import Blueprint, request
from .actions import public_login, public_get_documents, public_list_users, public_list_user, public_get_user_tasks, public_complete_task, public_download_document
import json

public = Blueprint(
    'public', __name__
)

@public.route('/api/v2/public/login', methods=["POST"])
def api_public_login():
    post_data = request.json
    try:
        username = post_data["username"]
        password = post_data["password"]
    except:
        return {"result":"failed","message":"Username and password combination required."}
    
    return public_login(username, password)

@public.route('/api/v2/public/users', methods=["GET"])
def api_public_list_users():
    try:
        token = request.headers.get("Authorization")
    except:
        return {"result":"failed", "message":"Request not authorized."}, 403
    
    return public_list_users(token)

@public.route('/api/v2/public/documents', methods=["GET"])
def api_public_fetch_documents():
    try:
        token = request.headers.get("Authorization")
    except:
        return {"result":"failed", "message":"Request not authorized."}, 403
    
    return public_get_documents(token)

@public.route('/api/v2/public/document/<document>/download', methods=["GET"])
def api_public_document_download(document):
    try:
        token = request.headers.get("Authorization")
    except:
        return {"result":"failed", "message":"Request not authorized."}, 403
    
    return public_download_document(document, token)


@public.route('/api/v2/public/user/<username>/info', methods=["GET"])
def api_public_list_user(username):
    try:
        token = request.headers.get("Authorization")
    except:
        return {"result":"failed", "message":"Request not authorized."}, 403
    
    if len(username) == 0:
        return {"result":"failed", "message":"Missing username parameter."}, 400
    
    return public_list_user(token, username)
    
@public.route('/api/v2/public/user/<user_uuid>/tasks', methods=["GET"])
def api_public_get_user_tasks(user_uuid):
    try:
        token = request.headers.get("Authorization")
    except:
        return {"result":"failed", "message":"Request not authorized."}, 403
    
    if len(user_uuid) <= 1:
        return {"result":"failed", "message":"Invalid user ID provided."}, 400
    
    return public_get_user_tasks(token, user_uuid)

@public.route('/api/v2/public/task/<task_uuid>/complete', methods=["PATCH"])
def api_public_task_complete(task_uuid):
    try:
        token = request.headers.get("Authorization")
    except:
        return {"result":"failed", "message":"Request not authorized."}, 403
    
    if len(task_uuid) <= 1:
        return {"result":"failed", "message":"Invalid task ID provided."}, 400
    
    return public_complete_task(token, task_uuid)