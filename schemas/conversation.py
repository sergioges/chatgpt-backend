def contextEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "user_id": item["user_id"],
        "background": item["background"],
        "content": item["content"]
    }

def contextsEntity(entity) -> list:
    return [contextEntity(item) for item in entity]