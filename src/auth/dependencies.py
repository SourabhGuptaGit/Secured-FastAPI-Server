from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials

from src.auth.utils import decode_token


class TokenBearer(HTTPBearer):
    
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)
        
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        creds = await super().__call__(request)
        
        parsed_token = await decode_token(creds.credentials)
        print(f"{parsed_token = }")
        if (not parsed_token) or (not isinstance(parsed_token, dict)):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid/Expired token."
            )
        await self.verify_token_data(parsed_token)
        
        return creds
    
    async def verify_token_data(self, parsed_token: dict) -> bool:
        raise NotImplementedError("Backend Error: verify_token_data() should be overwritten.")
    

class AccessTokenBearer(TokenBearer):
    
    async def verify_token_data(self, parsed_token: dict) -> bool:
        if parsed_token.get("refresh"):
            print("\n\n\nwait i know this place\n\n\n")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Please provide the access token."
            )
        return True
    

class RefreshTokenBearer(TokenBearer):
    
    async def verify_token_data(self, parsed_token: dict) -> bool:
        if not parsed_token.get("refresh"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Please provide the refresh token."
            )
        return True