from fastapi import APIRouter, Response, status
from errors import control_errors
from config.db import connection
from schemas.user import userEntity, usersEntity
from models.user import User, UserEdit
from passlib.hash import sha256_crypt
from datetime import datetime
from bson import ObjectId
from bson.objectid import InvalidId
from starlette.status import HTTP_204_NO_CONTENT
from rich import print  # https://www.youtube.com/watch?v=4zbehnz-8QU
from rich.console import Console
import re

user = APIRouter()

console = Console()

# Get all users
@user.get(
    "/users",
    # TODO Check documentation for show model as a list
    # response_model=list[User],
    response_description="You can get all the users from DDBB",
    tags=["Users"],
)
def get_all_users():
    try:
        all_users = connection.chatgptDB.user.find()

        print("🎫")
        console.print("Someone made a request of all users", style="bold blue")
        print("☝️")

        return usersEntity(all_users)

    except Exception:
        control_errors(5)


# Create a new user
@user.post(
    "/users",
    response_model=User,
    response_description="You can create a new user",
    tags=["Users"],
)
def create_user(user: User):
        new_user = user.dict()
        if not new_user["name"]:
            control_errors(7)
        if not new_user["password"]:
            control_errors(8)

        new_user["password"] = sha256_crypt.encrypt(new_user["password"])
        new_user["registration"] = datetime.now()
        del new_user["id"]

        email_regex = r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
        if re.match(email_regex, user.email):
            email_registered = connection.chatgptDB.user.find_one(
                {"email": user.email}, {"_id": 0}
            )
        else:
            print("email format incorrect")
            control_errors(3)

        if email_registered:
            print("😤")
            console.print(f"The email {user.email} is already taken", style="bold blue")
            print("🤯")
            control_errors(4)
        else:
            user_id = connection.chatgptDB.user.insert_one(new_user).inserted_id
            user_created = connection.chatgptDB.user.find_one({"_id": user_id})

            # Update date format to dd/mm/aa
            user_created["registration"] = new_user["registration"].strftime("%d/%m/%y")

            print("😍")
            console.print("New user was created", style="bold blue")
            print(user_created)
            print("🎯")

            return userEntity(user_created)


# Get a specific user
@user.get(
    "/users/{id}",
    response_model=User,
    response_description="You can get a specific user by the ID",
    tags=["Users"],
)
def get_user(id: str):
    try:
        database_user = connection.chatgptDB.user.find_one({"_id": ObjectId(id)})

        print("🙋‍♂️")
        console.print("Someone made a request of a specific user", style="bold blue")
        print("🙏")
        return userEntity(database_user)

    except InvalidId:
        control_errors(2)
    except Exception:
        control_errors(6)


# Update a specific user
@user.put(
    "/users/{id}",
    response_model=UserEdit,
    response_description="You can update a specific user by the ID",
    tags=["Users"],
)
def update_user(id: str, userEdit: UserEdit):
    try:
        edited_user = userEdit.dict()
        del edited_user["id"]
        del edited_user["registration"]

        database_user = connection.chatgptDB.user.find_one({"_id": ObjectId(id)})

        if not edited_user["name"]:
            edited_user["name"] = database_user["name"]

        # TODO Validate the correct email format
        if not edited_user["email"]:
            edited_user["email"] = database_user["email"]

        if not edited_user["password"]:
            edited_user["password"] = database_user["password"]
        else:
            edited_user["password"] = sha256_crypt.encrypt(edited_user["password"])

        edited_user["registration"] = database_user["registration"]

        # if not sha256_crypt.verify(edited_user["password"], database_user["password"]):
        #     edited_user["password"] = sha256_crypt.encrypt(edited_user["password"])
        # else:
        #     edited_user["password"] = database_user["password"]

        connection.chatgptDB.user.find_one_and_update(
            {"_id": ObjectId(id)}, {"$set": edited_user}
        )

        user_updated = connection.chatgptDB.user.find_one({"_id": ObjectId(id)})
        print("⛔")
        console.print("An user data was updated", style="bold blue")
        print(user_updated)
        print("✔️")

        return userEntity(user_updated)

    except InvalidId:
        control_errors(2)
    except Exception:
        control_errors(6)


# Delete a specific user
@user.delete(
    "/users/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="You can delete a specific user by ID",
    tags=["Users"],
)
def delete_user(id: str):
    try:
        database_user = connection.chatgptDB.user.find_one({"_id": ObjectId(id)})

        userEntity(connection.chatgptDB.user.find_one_and_delete({"_id": ObjectId(id)}))

        print("😭")
        console.print("We lost a user", style="bold blue")
        print(database_user)
        print("❌")

        return Response(status_code=HTTP_204_NO_CONTENT)

    except InvalidId:
        control_errors(2)
    except Exception:
        control_errors(6)
