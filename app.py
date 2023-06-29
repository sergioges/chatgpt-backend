from fastapi import FastAPI # https://www.youtube.com/watch?v=4e2VW3Nu-64
from fastapi.middleware.cors import CORSMiddleware
from routes import conversation, user, questions, login, gallery
from docs import tags_metadata
from dotenv import load_dotenv

# init environment in cmd | conda activate api-chatgpt / https://www.youtube.com/watch?v=aE7qxfgubS8
# init app with | uvicorn app:app --reload / https://www.youtube.com/watch?v=_eWEmRWhk9A
# pip freeze > requirements.txt for updating the requirements
# discard environment | conda deactivate

# deploy app in Heroku https://www.youtube.com/watch?v=4hS0YOZD-g4

app = FastAPI(
    title="API conversation by chatGPT",
    description="Backend structure for generating conversations with chatGPT and creating images background context using Unsplash API",
    version="0.0.1",
    openapi_tags=tags_metadata
)

# Configurar los encabezados CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

load_dotenv()

app.include_router(user.user)

app.include_router(conversation.conversation)

app.include_router(questions.questions)

app.include_router(login.login)

app.include_router(gallery.gallery)
