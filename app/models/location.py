from pydantic import BaseModel, Field, validator
from typing import List

class Location(BaseModel):
    """
    userコレクションモデル(CREATE)
    """
    type: str = Field("Point")
    coordinates: List[float] = Field(None, title="経度, 緯度")

    @validator("coordinates")
    def coordinates_lng_lat(cls, v):
        if len(v) != 2:
            raise ValueError("length of coordinates needs to be 2")
        if not 180 >= v[0] >= -180:
            raise ValueError("lng needs to be between -180 and 180") 
        if not 90 >= v[1] >= -90:
            raise ValueError("lat needs to be between -90 and 90") 
        return v