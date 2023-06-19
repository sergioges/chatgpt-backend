from fastapi import Request, Header  # https://www.youtube.com/watch?v=Of1V5JV6voc
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from jwt import decode, exceptions
from os import getenv
from errors import error_list, control_errors

def verify_token(Authorization: str = Header(None)):
    try:
        if "Bearer" in Authorization:
            auth = Authorization.split(" ")[1]
            return decode(auth, key=getenv("LOGIN_SECRET"), algorithms=["HS256"])
        else:
            return decode(Authorization, key=getenv("LOGIN_SECRET"), algorithms=["HS256"])
    except exceptions.DecodeError:
        return JSONResponse(status_code=401, content=error_list[1])
    except exceptions.ExpiredSignatureError:
        return JSONResponse(status_code=429, content=error_list[5])
    except Exception:
        control_errors(6)

            
class VerifyToken(APIRoute):
    def get_route_handler(self):
        route_handler = super().get_route_handler()
        async def auth_wrapper(request: Request):
            headers = request.headers
            authorization = headers.get("authorization")
            user_verified = verify_token(authorization)
            if isinstance(user_verified, dict):
                response = await route_handler(request)
                return response
            else:
                return verify_token(authorization)
        return auth_wrapper
