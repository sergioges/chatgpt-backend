from fastapi import APIRouter
from middlewares.verify_token import VerifyToken
from errors import questions_errors
from config.db import connection
from schemas.questions import questionEntity, questionsEntity
from models.questions import Question, QuestionEdit
from datetime import datetime
from bson import ObjectId
from bson.objectid import InvalidId
from rich import print
from rich.console import Console

# route_class=VerifyToken
questions = APIRouter(route_class=VerifyToken)

user_data = {}
user_questions = []
console = Console()


@questions.get(
    "/questions",
    response_description="You can get all the user's questions from DDBB",
    tags=["Questions"],
)
def get_all_questions():
    try:
        all_questions = questionsEntity(connection.chatgptDB.questions.find())

        console.print("All users questions", style="bold blue")
        print("❓")
        print(all_questions)
        print("👫")

        return all_questions

    except Exception as error:
        questions_errors(error, 5)


@questions.post(
    "/questions/{user_id}",
    response_description="Add new questions in DDBB from a specific user",
    tags=["Questions"],
)
def add_user_questions(user_id: str, question: Question):
# TODO Evitar que se guarden preguntas con ids de usuarios alterados y si son alterados devolver un error 404
    try:
        if connection.chatgptDB.questions.find_one({"user_id": user_id}):
            user_data = questionEntity(
                connection.chatgptDB.questions.find_one({"user_id": user_id})
            )
            
            user_questions = user_data["questions"]
            dict_question = question.dict()
            obj_id = ObjectId()
            new_question = {
                "question_id": str(obj_id),
                "role": dict_question["role"],
                "content": dict_question["content"],
                "registration": datetime.now(),
                "update": False
            }
            user_questions.append(new_question)

            if user_data["clear_questions"] == "":
                clear_date = ""
            else:
                clear_date = user_data["clear_questions"]

            connection.chatgptDB.questions.find_one_and_update(
                {"user_id": user_data["user_id"]},
                {
                    "$set": dict(
                        {
                            "user_id": user_data["user_id"],
                            "clear_questions": clear_date,
                            "questions": user_questions,
                        }
                    )
                },
            )

            user_data = questionEntity(
                connection.chatgptDB.questions.find_one({"user_id": user_id})
            )
            print(user_data)
            return user_data
        else:
            dict_question = question.dict()
            add_question = []
            obj_id = ObjectId()
            new_question = {
                "question_id": str(obj_id),
                "role": dict_question["role"],
                "content": dict_question["content"],
                "registration": datetime.now(),
            }
            add_question.append(new_question)
            clear_date = ""
            connection.chatgptDB.questions.insert_one(
                {
                    "user_id": user_id,
                    "clear_questions": clear_date,
                    "questions": add_question,
                }
            )
            user_data = questionEntity(
                connection.chatgptDB.questions.find_one({"user_id": user_id})
            )
            print(user_data)
            return user_data

    except InvalidId as error:
        questions_errors(error, 2)
    except Exception as error:
        questions_errors(error, 6)


# TODO Si hemos borrado todas las preguntas y queremos editar una que existía previamente, no genera error y devuelve
# {
#     "id": "645631fda3f281429c45fc80",
#     "user_id": "64563115a3f281429c45fc7e",
#     "clear_questions": "2023-05-06T13:14:41.661000",
#     "questions": []
# }
@questions.put(
    "/questions/{user_id}",
    response_description="Update an specific question from a specific user in the DDBB",
    tags=["Questions"],
)
def update_user_question(user_id: str, question: QuestionEdit):
    try:
        user_data = questionEntity(
            connection.chatgptDB.questions.find_one({"user_id": user_id})
        )

        user_questions = user_data["questions"]
        dict_question = question.dict()

        for question_database in user_questions:
            if dict_question["question_id"] == question_database["question_id"]:
                question_database["content"] = dict_question["content"]
                question_database["update"] = False

        if user_data["clear_questions"] == "":
            clear_date = ""
        else:
            clear_date = user_data["clear_questions"]

        connection.chatgptDB.questions.find_one_and_update(
            {"user_id": user_data["user_id"]},
            {
                "$set": dict(
                    {
                        "user_id": user_data["user_id"],
                        "clear_questions": clear_date,
                        "questions": user_questions,
                    }
                )
            },
        )

        return user_data

    except InvalidId as error:
        questions_errors(error, 2)
    except Exception as error:
        questions_errors(error, 6)


@questions.get(
    "/questions/{user_id}",
    response_description="You can get all questions from a specific user by ID",
    tags=["Questions"],
)
def get_user_questions(user_id: str):
    try:
        user_data = questionEntity(
            connection.chatgptDB.questions.find_one({"user_id": user_id})
        )

        console.print("Get questions from specific user", style="bold blue")
        print("❓")
        print(user_data)
        print("🙋‍♂️")

        return user_data

    except InvalidId as error:
        questions_errors(error, 2)
    except Exception as error:
        questions_errors(error, 6)


@questions.delete(
    "/questions/{user_id}/{question_id}",
    response_description="You can delete an specific question of a specific user by ID",
    tags=["Questions"],
)
def delete_specific_question(user_id: str, question_id:str):
    try:
        user_data = questionEntity(
            connection.chatgptDB.questions.find_one({"user_id": user_id})
        )

        user_questions = user_data["questions"]
        for question_database in user_questions:
            if question_id == question_database["question_id"]:
                user_questions.remove(question_database)

        connection.chatgptDB.questions.find_one_and_update(
            {"user_id": user_data["user_id"]},
            {
                "$set": dict(
                    {
                        "user_id": user_data["user_id"],
                        "questions": user_questions,
                    }
                )
            },
        )
        
        user_questions.reverse()
        return user_questions

    except InvalidId as error:
        questions_errors(error, 2)
    except Exception as error:
        questions_errors(error, 6)


@questions.delete(
    "/questions/{user_id}",
    response_description="You can delete all questions from a specific user by ID",
    tags=["Questions"],
)
def delete_all_user_questions(user_id: str):
    try:
        user_questions = []
        clear_date = datetime.now()
        connection.chatgptDB.questions.find_one_and_update(
            {"user_id": user_id},
            {
                "$set": dict(
                    {
                        "user_id": user_id,
                        "clear_questions": clear_date,
                        "questions": user_questions,
                    }
                )
            },
        )

        console.print("Delete questions from specific user", style="bold blue")
        print("❓")
        print({"clear_date": clear_date})
        print("🙋🙅")

        return {"clear_date": clear_date}

    except InvalidId as error:
        questions_errors(error, 2)
    except Exception as error:
        questions_errors(error, 6)


def print_user_questions(user_data):
    console.print("Add user questions in database", style="bold blue")
    print("❓")
    print(user_data)
    print("➕")
