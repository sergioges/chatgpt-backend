def userEntity(user) -> dict:
    return {
        "id": str(user["_id"]), # _id id structure came from mongoDB
        "name": user["name"],
        "email": user["email"],
        "password": user["password"],
        "registration": user["registration"],
        "active": user["active"]
    }

def usersEntity(entity) -> list:
    return [userEntity(user) for user in entity]