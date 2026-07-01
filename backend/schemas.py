from pydantic import BaseModel, ConfigDict # used to configure schemas
from typing import Optional # used to define optional fields
import datetime # used to find the current date

class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True) # allows Pydantic schemas to read from SQLAlchemy model objects

class HallResponse(BaseSchema): # used in /halls route to define each individual hall
    id: int
    name: str
    slug: str

class ItemDetailResponse(BaseSchema): # used in /items/{id} to define each item specifically
    name: str
    rarity: Optional[str]
    last_seen: Optional[datetime.date]
    calories: float
    protein: float
    fat: Optional[float]
    carbs: Optional[float]
    hall_name: str

class MenuResponse(BaseSchema): # used in /menu to define all items in the current menu
    item_id: int
    calories: float
    protein: float
    fat: Optional[float]
    carbs: Optional[float]
    name: str

class SearchItemResponse(BaseSchema): # used in /items/search to define a specific searched item 
    name: str
    calories: float
    protein: float
    fat: Optional[float]
    carbs: Optional[float]

class UserResponse(BaseSchema):
    id: int
    first_name: str
    last_name: str
    email: str
    profile_picture: Optional[str]

class RatingRequest(BaseModel):
    score: int

class RatingResponse(BaseSchema):
    score: float
    count: int