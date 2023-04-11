def user_schema(user) -> dict:
    return {
        "id": str(user['_id']),
        "username": user['username'],
        "email": user['email']
    }

def users_schema(users) -> list:
    users_list = []
    for user in users:
        users_list.append(user_schema(user))
    
    return users_list