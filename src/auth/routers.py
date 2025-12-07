from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List

from src.auth.schemas import UserModel, UserCreateModel
from src.auth.services import UserService
from src.db.db_agent import get_session


auth_router = APIRouter()

def get_user_service():
    return UserService()


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