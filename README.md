# Teammate --> Your Professional Assistant

   ![Badge en VERSION](https://img.shields.io/badge/VERSION-1.0.0-blue) ![Badge en LICENCIA](https://img.shields.io/badge/LICENSE-MIT-yellow) ![Badge en LICENCIA](https://img.shields.io/badge/RELEASE%20DATE-JULY%202023-green)

![Teammate -- Your Professional Assistant](https://github.com/sergioges/teammate/blob/main/public/logo_readme.png?raw=true)

## Description
**Backend structure** that generates conversations through the [chatGPT](https://platform.openai.com/) engine (API), in addition to connecting with the [Unsplash](https://unsplash.com/developers) Gallery API to provide visual content and enrich the generated conversations. 

The tool's intention is to provide a secure environment for the user, where their queries, conversation context, and personalized image from the front-end are stored in a database. 

The stored queries can be updated, resent as new queries, and removed from the list, ensuring that the queries section is always up-to-date according to the user's preferences.

In the Gallery section, the user can make a query to the Unsplash API to obtain high-quality graphical material under the _Creative Commons_ license, enhancing the queries made to the chatGPT API.

## Technology employed
- **Conda** --> v^23.3
- **Python** --> v^3.11
- **Uvicorn** --> v^0.21
- **FastAPI** --> v^0.95
- **Pydantic** --> v^1.10
- **Pyjwt** --> v^2.6
- **Pymongo** --> v^4.3
- **httpx** --> v^0.23
- **Python-dotenv** --> v^1.0
- More references --> [requirements.txt](https://github.com/sergioges/teammate-backend/blob/main/requirements.txt)

## Execution method
1. To create a virtual environment (to work with a specific version of Python, we use conda)\
`conda activate api-chatgpt`

2. Execute requirements to install the necessary instances in a virtual environment\
`pip install -r requirements.txt`

3. Run the app\
`uvicorn app:app --reload`

## Tutorials
|Concept | Link |
|--       |--    |
Install Conda | https://www.youtube.com/watch?v=aE7qxfgubS8
Use Uvicorn | https://www.youtube.com/watch?v=_eWEmRWhk9A
Use FastAPI | https://www.youtube.com/watch?v=4e2VW3Nu-64
How it works token middleware | https://www.youtube.com/watch?v=Of1V5JV6voc
Install MongoDB | http://www.youtube.com/watch?v=fZgJHJO81dw
Rich console | https://www.youtube.com/watch?v=4zbehnz-8QU
Deploy on Heroku | https://www.youtube.com/watch?v=4hS0YOZD-g4