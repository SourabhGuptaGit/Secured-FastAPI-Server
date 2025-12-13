from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from typing import List

from src.auth.utils import get_password_hash, verify_password
from src.auth.models import User, ROLES
from src.auth.schemas import UserCreateModel



class UserService:
    async def get_all_users(self, session: AsyncSession) -> List[User]:
        statement = select(User).order_by(desc(User.username))
        result = await session.exec(statement)
        return result.all()
    
    async def get_user_by_email(self, email: str, session: AsyncSession) -> User|None:
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        return result.first()
    
    async def create_user(self, user_data: UserCreateModel, session: AsyncSession) -> User|None:
        user_data_dict = user_data.model_dump()
        user_data_dict["password_hash"] = get_password_hash(user_data_dict["password"])
        del user_data_dict["password"]
        new_user_data = User(**user_data_dict)
        new_user_data.role = ROLES.USER.value
        session.add(new_user_data)
        await session.commit()
        return new_user_data