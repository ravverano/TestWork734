from fastapi import FastAPI, Request, Header, HTTPException, Depends
from starlette.status import HTTP_403_FORBIDDEN
from fastapi.security.api_key import APIKeyHeader
from config import settings

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

async def validate_api_key (
    authorization: str = Depends(api_key_header)
):
    if not authorization :
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Unauthorized: missing API key"
        )
    
    prefix = "ApiKey "
    if not authorization.startswith(prefix):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Unauthorized: Invalid API key format"
        )
    
    api_key = authorization[len(prefix):]
    if (
        api_key != settings.API_KEY
    ):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Unauthorized: Invalid API key"
        )
