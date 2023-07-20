def registerEntity(register) -> dict:
    return {
        "id": str(register["_id"]), # _id id structure came from mongoDB
        "email": register["email"],
        "registration": register["registration"]
    }