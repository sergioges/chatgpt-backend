from fastapi import APIRouter, HTTPException
from middlewares.verify_token import VerifyToken
import httpx
from urllib.parse import urlencode
from models.gallery import NextPage, NextPage_response
from errors import error_list
from os import getenv
from rich import print  # https://www.youtube.com/watch?v=4zbehnz-8QU
from rich.console import Console
from typing import List, Dict

# route_class=VerifyToken
gallery = APIRouter(route_class=VerifyToken)

console = Console()

@gallery.get(
    "/gallery/{query}",
    response_description="Call Unsplash API for getting the images",
    tags=["Gallery"],
)
async def get_gallery(query: str):
    unsplash_api_key = getenv("UNSPLASH_API_KEY")
    headers = {"Authorization": f"Client-ID {unsplash_api_key}"}
    parse_query = urlencode({"query": query})
    unsplash_results = {
                "gallery": [],
                "next_page_url": ''
            }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.unsplash.com/search/photos?order_by=relevant&per_page=20",
                headers=headers,
                params=parse_query,
            )

            link_header = response.headers.get('Link')
            next_page_url = ''
            if link_header:
                links = link_header.split(',')
                for link in links:
                    if 'rel="next"' in link:
                        next_page_url = link.split(';')[0].strip()[1:-1]
                        break
            
            if next_page_url:
                unsplash_results["next_page_url"] = next_page_url
            else:
                unsplash_results["next_page_url"] = ''

            response.raise_for_status()
            response_formatted = response.json()

            for picture in response_formatted["results"]:
                unsplash_results["gallery"].append(
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
            
@gallery.post(
    "/gallery",
    # response_model=Dict[str, NextPage_response],
    response_description="Call Unsplash API next page",
    tags=["Gallery"],
)
async def get_next_page(next_page: NextPage):
    unsplash_api_key = getenv("UNSPLASH_API_KEY")
    headers = {"Authorization": f"Client-ID {unsplash_api_key}"}
    unsplash_results = {
                "gallery": [],
                "next_page_url": ''
            }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{next_page.url}",
                headers=headers,
            )

        link_header = response.headers.get('Link')
        next_page_url = ''
        if link_header:
            links = link_header.split(',')
            for link in links:
                if 'rel="next"' in link:
                    next_page_url = link.split(';')[0].strip()[1:-1]
                    break
        
        if next_page_url:
            unsplash_results["next_page_url"] = next_page_url
        else:
            unsplash_results["next_page_url"] = ''

        response.raise_for_status()
        response_formatted = response.json()

        for picture in response_formatted["results"]:
            unsplash_results["gallery"].append(
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
            