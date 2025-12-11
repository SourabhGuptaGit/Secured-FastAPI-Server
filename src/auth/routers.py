from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from datetime import datetime, timedelta

from src.auth.schemas import UserLoginModel, UserModel, UserCreateModel
from src.auth.services import UserService
from src.db.db_agent import get_session
from src.auth.utils import verify_password, create_access_token, decode_token
from src.auth.dependencies import AccessTokenBearer, RefreshTokenBearer


auth_router = APIRouter()

def get_user_service():
    return UserService()

access_token_bearer = AccessTokenBearer()
refresh_token_bearer = RefreshTokenBearer()


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
    
    access_token = create_access_token(
        user_data={
            "email": email,
            "user_uid": str(existing_user_data.uid)
        }
    )
    
    refresh_token = create_access_token(
        user_data={
            "email": email,
            "user_uid": str(existing_user_data.uid)
        },
        refresh=True,
        expiry=5*3600
    )
    
    return JSONResponse(
        content={
            "message": "Login successful !!",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "email": email,
                "uid": str(existing_user_data.uid)
            }
        }
    )
    
# {'email': 'sourabh.admin@test.com', 'user_uid': 'b93d2588-6704-4ed4-9b63-d14edfa136cc'}, \
# 'exp': 1765493412, 'jti': '945e372b-00d8-4e34-82d6-f6b2d6f228e1', 'refresh': True}
@auth_router.get("/refresh_access_token")
async def refresh_access_token(refresh_user_details: RefreshTokenBearer = Depends(RefreshTokenBearer())):
    print(f"{refresh_user_details = }")
    parsed_token = await decode_token(refresh_user_details.credentials)
    print(f"{parsed_token = }")
    user_details = parsed_token.get("user")
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