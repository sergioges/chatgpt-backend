import smtplib
from email.mime.text import MIMEText
from config.db import connection
from os import getenv
from dotenv import load_dotenv
from fastapi import APIRouter
from errors import control_errors
from schemas.landing import registerEntity
from models.landing import Register
from datetime import datetime
from rich import print
from rich.console import Console
import re

# change_stream = connection.chatgptDB.landing.watch(full_document='updateLookup')
# print(change_stream)

def send_email(recipient_email):
    load_dotenv()
    smtp_server = getenv("SMTP_SERVER")
    smtp_port = getenv("SMTP_PORT")
    sender_email = getenv("SENDER_EMAIL")
    sender_password = getenv("SENDER_PASSWORD")

    subject = 'Nuevo registro en la BBDD de Landing'
    body = 'Se ha insertado un nuevo registro en la colección.'

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, recipient_email, msg.as_string())
    server.quit()

# for change in change_stream:
#   if change['operationType'] == 'insert':
#       send_email()

register = APIRouter()
console = Console()

# Create a new landing register
@register.post(
    "/register",
    response_model=Register,
    response_description="email registration from landing page",
    tags=["Register"],
)
def create_register(register: Register):
    new_register = register.dict()
    new_register["registration"] = datetime.now()
    del new_register["id"]

    email_regex = r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
    if re.match(email_regex, register.email):
        email_registered = connection.chatgptDB.landing.find_one(
            {"email": register.email}, {"_id": 0}
        )
    else:
        print("email format incorrect")
        control_errors(3)

    if email_registered:
        print("😤")
        console.print(f"The email {register.email} is already taken", style="bold blue")
        print("🤯")
        control_errors(4)
    else:
        register_id = connection.chatgptDB.landing.insert_one(new_register).inserted_id
        register_created = connection.chatgptDB.landing.find_one({"_id": register_id})
        # send_email(register.email)
        
        print("😍")
        console.print("New register was created", style="bold blue")
        print(register_created)
        print("🎯")

        return registerEntity(register_created)
    