def questionEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "user_id": item["user_id"],
        "clear_questions": item["clear_questions"],
        "questions": item["questions"]
    }

def questionsEntity(entity) -> list:
    return [questionEntity(item) for item in entity]