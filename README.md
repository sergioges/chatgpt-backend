# Teammate --> Your Professional Assistant

   ![Badge en VERSION](https://img.shields.io/badge/VERSION-1.0.0-blue) ![Badge en LICENCIA](https://img.shields.io/badge/LICENSE-MIT-yellow) ![Badge en LICENCIA](https://img.shields.io/badge/RELEASE%20DATE-JULY%202023-green)

![Teammate -- Your Professional Assistant](https://github.com/sergioges/teammate/blob/main/public/logo_readme.png?raw=true)

## Descripción
**Estructura backend** que genera conversaciones a través del motor (API) de [chatGPT](https://platform.openai.com/), además de conectar con la API de la galería CC [Unsplash](https://unsplash.com/developers) para proporcionar contenido visual y así enriquecer las conversaciones generadas.

La intención de la herramienta es proporcionar un entorno seguro al usuario, donde queda registrado en una base de datos sus consultas, el contexto de la conversación y la imagen que personalizada la app desde el lado de front.

Las consultas almacenadas pueden ser actualizadas, reenviadas como nuevas consultas y eliminadas de la lista, para así tener el apartado de consultas siempre actualizado por el propio usuario.

En el apartado de Galería, podrá hacer una consulta a la API de Unsplash, para obtener material gráfico de calidad bajo el estatuto de _Creative Commons_, para que pueda enriquecer las consultas realizadas a la API de chatGPT.

## Tecnología utilizada
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

## Forma de ejecutarse
1. Crear un entorno virtual (Para trabajar la versión de python específica utilizamos conda)\
`conda activate api-chatgpt`

2. Ejecutar requirements para instalar las instancias necesarias en un entorno virtual\
`pip install -r requirements.txt`

3. Arrancar la aplicación\
`uvicorn app:app --reload`

## Tutoriales
|Concepto | Link |
|--       |--    |
Install Conda | https://www.youtube.com/watch?v=aE7qxfgubS8
Use Uvicorn | https://www.youtube.com/watch?v=_eWEmRWhk9A
Use FastAPI | https://www.youtube.com/watch?v=4e2VW3Nu-64
How it works token middleware | https://www.youtube.com/watch?v=Of1V5JV6voc
Install MongoDB | http://www.youtube.com/watch?v=fZgJHJO81dw
Rich console | https://www.youtube.com/watch?v=4zbehnz-8QU
Deploy on Heroku | https://www.youtube.com/watch?v=4hS0YOZD-g4