from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
import datetime

class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class HallResponse(BaseSchema):
    id: int
    name: str
    slug: str

class ItemResponse(BaseSchema):
    id: int
    rarity: Optional[str]
    last_seen: Optional[str]

class ItemDetailResponse(BaseSchema):
    name: str
    rarity: Optional[str]
    last_seen: Optional[datetime.date]
    calories: float
    protein: float
    fat: Optional[float]
    carbs: Optional[float]
    hall_name: str

class MenuResponse(BaseSchema):
    item_id: int
    calories: float
    protein: float
    fat: Optional[float]
    carbs: Optional[float]
    name: str

class SearchItemResponse(BaseSchema):
    name: str
    calories: float
    protein: float
    fat: Optional[float]
    carbs: Optional[float]