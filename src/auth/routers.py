from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from datetime import datetime, timedelta

from src.auth.schemas import UserBooksModel, UserLoginModel, UserModel, UserCreateModel
from src.auth.services import UserService
from src.db.db_agent import get_session
from src.auth.utils import verify_password, create_access_token
from src.auth.dependencies import AccessTokenBearer, RefreshTokenBearer, get_current_auth_user, RoleChecker
from src.db.redis import add_token_to_blocklist
from src.auth.models import User, ROLES


auth_router = APIRouter()

def get_user_service():
    return UserService()

access_token_bearer = AccessTokenBearer()
refresh_token_bearer = RefreshTokenBearer()
role_checker = RoleChecker([ROLES.ADMIN.value, ROLES.USER.value])


@auth_router.get("/users", response_model=List[UserModel], status_code=status.HTTP_200_OK)
async def get_all_users(
    user_service: UserService = Depends(get_user_service),
    session: AsyncSession = Depends(get_session)
    ):
    users_data = await user_service.get_all_users(session)
    return users_data


@auth_router.post("/signup", response_model=UserModel, status_code=status.HTTP_201_CREATED)
async def create_user_account(
    user_data: UserCreateModel,
    user_service: UserService = Depends(get_user_service),
    session: AsyncSession = Depends(get_session)
    ):
    user_email = user_data.email
    existing_user_data = await user_service.get_user_by_email(user_email, session)
    if existing_user_data:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User with email - '{user_email}' already exists")
    
    new_user_data = await user_service.create_user(user_data, session)
    return new_user_data


@auth_router.post("/login")
async def create_user_session(
    user_data: UserLoginModel,
    user_service: UserService = Depends(get_user_service),
    session: AsyncSession = Depends(get_session)
    ):
    
    email = user_data.email
    existing_user_data = await user_service.get_user_by_email(email, session)
    if not existing_user_data:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please signup first!")
    
    valid_password = verify_password(user_data.password, existing_user_data.password_hash)
    if not valid_password:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid password!")
    
    user_data={
            "email": email,
            "user_uid": str(existing_user_data.uid),
            "role": ROLES.USER.value
        }
    access_token = create_access_token(
        user_data=user_data
    )
    
    refresh_token = create_access_token(
        user_data=user_data,
        refresh=True,
        expiry=5*3600
    )
    
    return JSONResponse(
        content={
            "message": "Login successful !!",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": user_data
        }
    )
    
# {'email': 'sourabh.admin@test.com', 'user_uid': 'b93d2588-6704-4ed4-9b63-d14edfa136cc'}, \
# 'exp': 1765493412, 'jti': '945e372b-00d8-4e34-82d6-f6b2d6f228e1', 'refresh': True}
@auth_router.get("/refresh_access_token")
async def refresh_access_token(user_details: dict = Depends(RefreshTokenBearer())):
    access_token = create_access_token(user_details)
    refresh_token = create_access_token(user_details, refresh=True)
    return JSONResponse(
        content={
            "message": "Tokens Refreshed !!",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": user_details
        }
    )


@auth_router.get("/me", response_model=UserBooksModel)
def get_current_user(
    user: User = Depends(get_current_auth_user),
    _: bool = Depends(role_checker)
    ):
    return user


@auth_router.get("/logout")
async def remove_user_session(access_user_details: dict = Depends(access_token_bearer)):
    await add_token_to_blocklist(access_user_details.get("jti"))
    return JSONResponse(
        content={
            "message": "Logout successfully!"
        }
    )