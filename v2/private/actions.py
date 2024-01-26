import sqlite3, string, random, time
from .admin_auth import create_token, is_authorized
from configuration import ConfigurationVariables

def generate_uuid():
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    uuid = ""
    for i in range(4):
        uuid += ''.join(random.choice(letters) for i in range(5))
        if i < 3:
            uuid += "-"
    return uuid

def connect_database():
    return sqlite3.connect(ConfigurationVariables.SQLITE3_DATABASE, isolation_level=None)

def private_login(username, password):
    try:
        db = connect_database()
        cursor = db.cursor()
        cursor.execute("SELECT `password` FROM `administratior_users` WHERE `username`=? LIMIT 1", (username,))
    except:
        return {"result":"failed", "message":"Error connecting to the database."}
    
    result = cursor.fetchone()
    try:
        if result[0] == password:
            return {"result":"success", "token": create_token("Administrator", username)}
    except:
        pass
    return {"result":"failed", "message":"Login attempt unsuccessful."}
def private_create_user(user_uuid, full_name, username, age, token):
    if not is_authorized(token):
        return {"result":"failed", "message":"Not authorized to perform this action."}, 403

    try:
        db = connect_database()
        cursor = db.cursor()
        result = cursor.execute("SELECT COUNT(`user_uuid`) as user_count FROM public_users WHERE username=?", (username,))
        if cursor.fetchone()[0] != 0:
            return {"result":"failed", "message":"Username already in use."}

        cursor.execute("INSERT INTO `public_users` (`user_uuid`,`username`,`full_name`,`age`,`password`) VALUES (?, ?, ?, ?, ?)", (user_uuid, username, full_name, age, generate_uuid().replace("-",""),))
    except:
        return {"result":"failed", "message":"Failed to add new user."}
    return {"result":"success", "message":"New user added."}

def private_delete_user(user_uuid, token_header):
    if not is_authorized(token_header):
        return {"result":"failed", "message":"Not authorized to perform this action."}, 403
    
    try:
        db = connect_database()
        cursor = db.cursor()
        cursor.execute("DELETE FROM `public_users` WHERE `user_uuid`=?", (user_uuid,))
    except:
        return {"result":"failed", "message":"Failed to delete user."}, 400
    return {"result":"success", "message":"User Deleted."}

def private_user_reset(new_password, user_uuid):
    try:
        db = connect_database()
        cursor = db.cursor()
        cursor.execute("UPDATE `public_users` SET `password`=? WHERE `user_uuid`=?", (new_password, user_uuid,))
    except:
        return {"result":"failed", "message":"Failed to reset the user."}
    return {"result":"success", "message":"User account reset."}

def create_private_task(task_title, task_details, assigned_user, token_header):
    if not is_authorized(token_header):
        return {"result":"failed", "message":"Not authorized to perform this action."}, 403
    
    try:
        db = connect_database()
        cursor = db.cursor()

        # SELECT uuid from username
        cursor.execute("SELECT `user_uuid` FROM `public_users` WHERE `username`=? LIMIT 1", (assigned_user,))
        user = cursor.fetchone()[0]
    except:
        return {"result":"failed", "message":"Failed to find user " + assigned_user + "."}, 400
    try:
        # INSERT task into database
        cursor.execute("INSERT INTO `tasks` (`task_uuid`,`task_title`,`task_details`,`assigned_user`,`task_status`) VALUES (?, ?, ?, ?, 'pending')", (generate_uuid(), task_title, task_details, user))
    except:
        return {"result":"failed", "message":"Task creation failed."}, 400
    
    return {"result":"success", "message":"Task created."}

def private_delete_task(task_uuid, token_header):
    if not is_authorized(token_header):
        return {"result":"failed", "message":"Not authorized to perform this action."}, 403
    
    try:
        db = connect_database()
        cursor = db.cursor()
        cursor.execute("DELETE FROM `tasks` WHERE `task_uuid`=?", (task_uuid,))
        cursor.close()
    except:
        return {"result":"failed", "message":"Failed to delete task."}, 400
    return {"result":"success", "message":"Task Deleted."}


def private_document_add(document, token_header):
    if not is_authorized(token_header):
        return {"result":"failed", "message":"Not authorized to perform this action."}, 403
    
    try:
        db = connect_database()
        cursor = db.cursor()
        cursor.execute("INSERT INTO `documents` VALUES (?, ?, ?, ?)", (generate_uuid(), document, str(time.time()),'',))
        cursor.close()
    except:
        return {"result":"failed", "message":"Failed to add document."}, 400
    
    return {"result":"success", "message":"New document added."}

def private_document_delete(document_uuid, token_header):
    if not is_authorized(token_header):
        return {"result":"failed", "message":"Not authorized to perform this action."}, 403
    
    try:
        db = connect_database()
        cursor = db.cursor()
        cursor.execute("DELETE FROM `documents` WHERE `document_uuid`=?", (document_uuid,))
        cursor.close()
        return {"result":"success", "message":"Document deleted."}
    except:
        return {"result":"failed", "message":"Failed to delete document."}, 400

def private_users_list(search, token_header):
    if not is_authorized(token_header):
        return {"result":"failed", "message":"Not authorized to perform this action."}, 403
    
    db = connect_database()
    cursor = db.cursor()
    results = []

    if search != None:
        for row in cursor.execute("SELECT `username`,`full_name`,`age`,`user_uuid` FROM `public_users` WHERE `username` LIKE '%" + str(search) + "%' OR `full_name` LIKE '%" + str(search) + "%'"):
            results.append({"username":row[0], "full_name":row[1], "age":row[2], "user_uuid":row[3]})
    else:
        for row in cursor.execute("SELECT `username`,`full_name`,`age`,`user_uuid` FROM `public_users`"):
            results.append({"username":row[0], "full_name":row[1], "age":row[2], "user_uuid":row[3]})
    return results

def private_list_tasks(token_header):
    if not is_authorized(token_header):
        return {"result":"failed", "message":"Not authorized to perform this action."}, 403
    
    db = connect_database()
    cursor = db.cursor()
    results = []

    for row in cursor.execute("SELECT `task_title`,`task_details`,`assigned_user`,`task_uuid`,`task_status` FROM `tasks`"):
        results.append({"task_title":row[0], "task_details":row[1], "assigned_user":row[2], "task_uuid":row[3], "task_status":row[4]})
    cursor.close()
    return results