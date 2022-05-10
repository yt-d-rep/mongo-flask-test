from pydantic import BaseModel, Field

from app.models.custom_type import PydanticObjectId



class UserCreate(BaseModel):
    """
    userコレクションモデル(CREATE)
    """
    name: str = Field(..., max_length=255, title="名前")
    age: int = Field(..., gt=0, lt=999, title="年齢")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            PydanticObjectId: lambda v: str(v),
        }

class UserRead(UserCreate):
    """
    userコレクションモデル(READ)
    """
    id: PydanticObjectId = Field(None, alias="_id", title="id")
