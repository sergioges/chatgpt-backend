from fastapi import APIRouter, HTTPException
from middlewares.verify_token import VerifyToken
import httpx
import openai
from config.db import connection
from schemas.conversation import contextEntity
from schemas.user import userEntity
from models.conversation import (
    Context,
    Context_response,
    Conversation_response,
    SavedContext,
)
from models.questions import Question
from routes.questions import add_user_questions
from bson import ObjectId
from bson.objectid import InvalidId
from errors import error_list, control_errors
from os import getenv
from dotenv import load_dotenv
from rich import print  # https://www.youtube.com/watch?v=4zbehnz-8QU
from rich.console import Console
from typing import List, Dict

# route_class=VerifyToken
conversation = APIRouter(route_class=VerifyToken)
load_dotenv()

openai.api_key = getenv("CHATGPT_API_KEY")

console = Console()
conversations = []


# TODO Ver la estructura de la respuesta para la documentación response_model
# Create context and get background images
@conversation.post(
    "/context",
    # response_model=List[Context_response],
    response_description="Stablish the context for a initial conversation and get images for the app background",
    tags=["Conversation"],
)
async def create_context(context: Context):
    unsplash_api_key = getenv("UNSPLASH_API_KEY")
    try:
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Client-ID {unsplash_api_key}"}

            if context.content == '' or context.background == '':
                control_errors(0)

            response = await client.get(
                "https://api.unsplash.com/search/photos?page=1&per_page=6&order_by=relevant&orientation=landscape",
                headers=headers,
                params={"query": context.background},
            )
            response.raise_for_status()

            response_formatted = response.json()

            unsplash_results = []

            for picture in response_formatted["results"]:
                unsplash_results.append(
                    {
                        "image": {
                            "url": picture["urls"]["regular"],
                            "description": picture["alt_description"],
                        },
                        "user": {
                            "name": picture["user"]["name"],
                            "link": picture["user"]["links"]["html"],
                            "profile_image": picture["user"]["profile_image"]["medium"],
                        },
                    }
                )

            openai_context = {"role": context.role, "content": context.content}
            # Contexto inicial de la conversación
            conversations.append(openai_context)

            console.print("Unsplash API Results", style="bold blue")
            print("📷♡")
            print(unsplash_results)
            print("o👌k")

            return unsplash_results

    # Si se produce un error HTTP (por ejemplo, 404 Not Found), devolver una respuesta de error adecuada
    except httpx.HTTPStatusError as exc:
        error_code = exc.response.status_code
        for error in error_list:
            if error["code"] == error_code:
                raise HTTPException(status_code=error_code, detail=error)
    # Si se produce un error de solicitud (por ejemplo, no se pudo conectar al servidor), devolver una respuesta de error adecuada
    except httpx.RequestError as exc:
        error_code = exc.response.status_code
        for error in error_list:
            if error["code"] == error_code:
                raise HTTPException(status_code=error_code, detail=error)

# Get context from BBDD
@conversation.get(
    "/context/saved/{user_id}",
    response_description="Recover image background and initial conversation context from DDBB",
    tags=["Conversation"],
)
def get_context(user_id: str):
    try:
        control_user = userEntity(
            connection.chatgptDB.user.find_one({"_id": ObjectId(user_id)})
        )

        context_data = contextEntity(
                connection.chatgptDB.context.find_one({"user_id": control_user["id"]})
            ) 
        # TODO Identificar como se puede dirigir a un error en específico si context_data no existe

        console.print("User background image and context from de DDBB", style="bold blue")
        print("👨🏼👨‍💻")
        print(context_data)
        print("o👌k")

        return context_data
    
    except InvalidId:
        control_errors(2)
    except Exception:
        control_errors(2)

# Create or update context from DDBB
@conversation.post(
    "/context/saved/{user_id}",
    response_description="Create or update image background and initial conversation context from DDBB",
    tags=["Conversation"],
)
def save_context(user_id: str, saved_context: SavedContext):
    try:
        context = saved_context.dict()
        control_user = userEntity(
            connection.chatgptDB.user.find_one({"_id": ObjectId(user_id)})
        )

        if connection.chatgptDB.context.find_one({"user_id": control_user["id"]}):

            connection.chatgptDB.context.find_one_and_update(
                {"user_id": control_user["id"]},
                {
                    "$set": dict(
                        {
                            "user_id": user_id,
                            "content": context["content"],
                            "background": context["background"],
                        }
                    )
                },
            )

            console.print("Update user background image and context from de DDBB", style="bold blue")
            print("👨🏼👨‍💻")
            print(context)
            print("o👌k")

            return context
        else:
            connection.chatgptDB.context.insert_one(
                {
                    "user_id": user_id,
                    "content": context["content"],
                    "background": context["background"],
                }
            )
            new_context = contextEntity(
                connection.chatgptDB.context.find_one({"user_id": user_id})
            )

            console.print("New user background image and context was created", style="bold blue")
            print("✍🏼")
            print(new_context)
            print("o👌k")

            return new_context
    except InvalidId:
        control_errors(2)
    except Exception:
        control_errors(6)


# Generate conversation with chatGPT API
@conversation.post(
    "/conversation/{user_id}",
    response_model=Conversation_response,
    response_description="You can get the answers from chatGPT related to the question you made and the context defined before",
    tags=["Conversation"],
)
def make_question(user_id: str, question: Question):
    new_question = question.dict()
    try:
        new_question = question.dict()

        if not new_question["content"]:
            return {"role": "assistant", "content": "You missed an inquiry"}
        else:
            # Contexto de todas las preguntas realizadas
            conversations.append(new_question)

            # Add questions to user database
            add_user_questions(user_id, question)
            
            response_chatgpt = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=conversations
            )

            response_content = response_chatgpt.choices[0].message.content

            # Contexto de todas las respuestas ofrecidas
            response_formatted = {"role": "assistant", "content": response_content}
            conversations.append(response_formatted)

            console.print("OpenAI API Conversation", style="bold blue")
            print("🤖")
            print(response_formatted)
            print("o👌k")

            return response_formatted

    except openai.error.AuthenticationError:
        raise HTTPException(status_code=error_list[0]["code"], detail=error_list[0])
    except openai.error.InvalidRequestError:
        raise HTTPException(status_code=error_list[2]["code"], detail=error_list[2])
    except openai.error.InvalidRequestError:
        raise HTTPException(status_code=error_list[3]["code"], detail=error_list[3])
