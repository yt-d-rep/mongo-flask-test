from pydantic import BaseModel, Field

from app.modules.custom_type import PydanticObjectId



class PostCreate(BaseModel):
    """
    postコレクションモデル(CREATE)
    """
    title: str = Field(..., max_length=32, title="タイトル")
    message: str = Field(..., max_length=255, title="本文")
    userId: PydanticObjectId = Field(..., title="ユーザID")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            PydanticObjectId: lambda v: str(v),
        }

class PostRead(PostCreate):
    """
    postコレクションモデル(READ)
    """
    id: PydanticObjectId = Field(..., alias="_id", title="id")