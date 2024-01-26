import sqlite3, base64
from .auth import create_token, is_authorized, authorization_info
from configuration import ConfigurationVariables

def connect_database():
    return sqlite3.connect(ConfigurationVariables.SQLITE3_DATABASE, isolation_level=None)

def public_login(username, password):
    try:
        db = connect_database()
        cursor = db.cursor()
        users = cursor.execute("SELECT `user_uuid`,`password` FROM `public_users` WHERE `username`=? LIMIT 1", (username,))
    except:
        return {"result":"failed", "message":"Error connecting to the database."}
    
    result = cursor.fetchone()
    if result[1] == password:
        return {"result":"success", "token": create_token(result[0], username)}
    else:
        return {"result":"failed", "message":"Login attempt unsuccessful."}
    
def public_list_users(token_header):
    if not is_authorized(token_header):
        return '{"result":"failed", "message":"No authorization token provided"}', 403
    
    db = connect_database()
    cursor = db.cursor()
    results = []
    for row in cursor.execute("SELECT `username`,`full_name`,`age` FROM `public_users`"):
        results.append({"username":row[0], "full_name":row[1], "age":row[2]})

    cursor.close()
    return results

def public_download_document(document, token_header):
    if not is_authorized(token_header):
        return {"result":"failed", "message":"No authorization token provided"}, 403
    
    try:
        db = connect_database()
        cursor = db.cursor()
        cursor.execute("SELECT `document_name` FROM `documents` WHERE `document_uuid`=? LIMIT 1", (document, ))
        document = cursor.fetchone()[0]
    except:
        return {"result":"failed", "message":"Failed to fetch document."}
    
    try:
        return {"result":"success", "message":"Document retrieved.", "contents":base64.b64encode(open(ConfigurationVariables.BASEDIR + "/documents/" + document).read().encode('utf-8')).decode('ascii')}
    except:
        return {"result":"failed", "message":"Failed to read the document."}

def public_list_user(token_header, username):
    if not is_authorized(token_header):
        return {"result":"failed", "message":"No authorization token provided"}, 403
    
    try:
        db = connect_database()
        cursor = db.cursor()
        results = []
        for row in cursor.execute("SELECT `user_uuid`,`username`,`age`,`full_name`,`bio`,`password` FROM `public_users` WHERE `username`=? LIMIT 1", (username,)):
            results.append({"user_uuid":row[0], "username":row[1], "age":row[2], "full_name":row[3], "bio":row[4],"password":''.join("*" for i in range(len(row[5])))})

        cursor.close()
    except:
        return '{"result":"failed", "message":"Unable to retrive user information."}'
    return results

def public_get_documents(token_header):
    if not is_authorized(token_header):
        return '{"result":"failed", "message":"No authorization token provided"}', 403
    
    token_information = authorization_info(token_header)
    db = connect_database()
    cursor = db.cursor()
    results = []
    for row in cursor.execute("SELECT `document_uuid`,`document_name`,`document_creation_date` FROM `documents`"):
        results.append({"document_uuid":row[0], "document_name":row[1], "document_creation_date":row[2]})

    cursor.close()
    return results

def public_get_user_tasks(token_header, user_uuid):
    if not is_authorized(token_header):
        return '{"result":"failed", "message":"No authorization token provided"}', 403
    
    db = connect_database()
    cursor = db.cursor()
    results = []
    for row in cursor.execute("SELECT * FROM `tasks` WHERE `assigned_user`=?", (user_uuid,)):
        results.append({"task_uuid":row[0], "task_name":row[1], "task_details":row[2], "assigned_user":row[3], "task_status":row[4]})

    cursor.close()
    return results

def public_complete_task(token_header, task_uuid):
    if not is_authorized(token_header):
        return '{"result":"failed", "message":"No authorization token provided"}', 403
    
    token_information = authorization_info(token_header)

    try:
        db = connect_database()
        cursor = db.cursor()

        cursor.execute("SELECT COUNT(`task_uuid`) AS `task_exists` FROM `tasks` WHERE `assigned_user`=? AND `task_uuid`=?", (token_information["user_uuid"], task_uuid,))
        result = cursor.fetchone()
        if result[0] != 1:
            return {"status":"failed", "message":"User not authorized to perform this action."}, 403

        cursor.execute("UPDATE `tasks` SET `task_status`='complete' WHERE `assigned_user`=? AND `task_uuid`=?", (token_information["user_uuid"], task_uuid,))
        cursor.close()
        return {"status":"successful", "message":"Task marked as complete."}
    except:
        return {"status":"failed", "message":"Unable to update task."}, 400