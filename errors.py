from fastapi import HTTPException

error_list = [
    {"code": 400, "message": "Bad request"},
    {"code": 401, "message": "Unauthorized access"},
    {"code": 404, "message": "Data not found"},
    {"code": 405, "message": "Email format incorrect"},
    {"code": 409, "message": "User already exists in our database"},
    {"code": 429, "message": "Rate limit access error"},
    {"code": 500, "message": "Something have failed"},
    {"code": 403, "message": "Name required"},
    {"code": 403, "message": "Password required"},
]

def questions_errors(response, index):
    if str(response).startswith(""):
        raise HTTPException(status_code=error_list[index]["code"], detail=error_list[index])
            
    for error in error_list:
        if str(response).startswith(str(error["code"])):
            raise HTTPException(status_code=error["code"], detail=error)
        
def control_errors(index):
    raise HTTPException(status_code=error_list[index]["code"], detail=error_list[index])
