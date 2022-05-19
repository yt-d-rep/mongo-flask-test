from pydantic import BaseModel, Field, confloat, validator
from typing import List

from app.modules.custom_type import PydanticObjectId
from app.models.post import PostRead
from app.models.location import Location

class UserField:
    id = Field(..., alias="_id", title="id")
    name = Field(None, max_length=255, title="名前")
    age = Field(None, gt=0, lt=999, title="年齢")
    age2 = Field(None, gt=0, lt=999, title="年齢")
    location = Field(None, title="位置")

class UserCreate(BaseModel):
    """
    userコレクションモデル(CREATE)
    """
    name: str = UserField.name
    age: int = UserField.age
    location: Location = UserField.location

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            PydanticObjectId: lambda v: str(v),
        }

class UserUpdate(UserCreate):
    """
    userコレクションモデル(UPDATE)
    """
    id: PydanticObjectId = UserField.id

class UserRead(UserCreate):
    """
    userコレクションモデル(READ)
    """
    id: PydanticObjectId = UserField.id


class UserReadWithPosts(UserRead):
    """
    userコレクションとpostコレクションのjoinモデル(READ)
    """
    posts: List[PostRead]
