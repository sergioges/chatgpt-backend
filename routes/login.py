from fastapi import APIRouter  # https://www.youtube.com/watch?v=Of1V5JV6voc
from errors import control_errors
from models.login import Login
from passlib.hash import sha256_crypt
from config.db import connection
from schemas.user import userEntity
from rich import print
from rich.console import Console

from jwt import encode
from datetime import datetime, timedelta
from os import getenv

login = APIRouter()

console = Console()


def expire_date(days: int):
    date = datetime.now()
    new_date = date + timedelta(days)
    return new_date


def write_token(user: dict):
    token = encode(
        payload={**user, "exp": expire_date(2)},
        key=getenv("LOGIN_SECRET"),
        algorithm="HS256",
    )
    return token

# TODO Falta personalizar la documentación
@login.post("/login")
def login_user(login: Login):
    user_login = login.dict()
    user_database = connection.chatgptDB.user.find_one({"email": user_login["email"]})
    access_granted = user_database and sha256_crypt.verify(
        user_login["password"], user_database["password"]
    )

    if access_granted:
        user_token = write_token(user_login)
        user_granted = userEntity(user_database)
        user_granted["token"] = user_token
        user_granted.pop("password")

        print("🙋‍♂️")
        console.print("Access granted", style="bold blue")
        console.print({"token": user_token})
        print("☝️")

        # Update date format to dd/mm/aa
        user_granted["registration"] = user_granted["registration"].strftime("%d/%m/%y")

        return user_granted
    else:
        print("🙋‍♂️")
        console.print("User or email invalid", style="bold blue")
        print("⛔")

        control_errors(1)
