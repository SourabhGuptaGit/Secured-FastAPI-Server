from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List

from src.auth.utils import decode_token
from src.db.redis import get_token_in_blocklist
from src.auth.services import UserService
from src.db.db_agent import get_session
from src.auth.models import User


def get_user_service():
    return UserService()

class TokenBearer(HTTPBearer):
    
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)
        
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        creds = await super().__call__(request)
        
        parsed_token = await decode_token(creds.credentials)
        if (not parsed_token) or (not isinstance(parsed_token, dict)):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid/Expired token."
            )

        if await get_token_in_blocklist(parsed_token.get("jti")):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token revoked (Logout)."
            )
            
        await self.verify_token_data(parsed_token)
        return parsed_token
    
    async def verify_token_data(self, parsed_token: dict) -> bool:
        raise NotImplementedError("Backend Error: verify_token_data() should be overwritten.")
    

class AccessTokenBearer(TokenBearer):
    
    async def verify_token_data(self, parsed_token: dict) -> bool:
        if parsed_token.get("refresh"):
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


async def get_current_auth_user(
    user_details: AccessTokenBearer = Depends(AccessTokenBearer()),
    user_service: UserService = Depends(get_user_service),
    session: AsyncSession = Depends(get_session)
    ):
    
    email = user_details.get("user").get("email")
    user_data = await user_service.get_user_by_email(email, session)
    return user_data


class RoleChecker:
    
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles
        
    async def __call__(self, current_user_details: User = Depends(get_current_auth_user)):
        if current_user_details.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: You do not have permission to perform this action."
            )
        return True