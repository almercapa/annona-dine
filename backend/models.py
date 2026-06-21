from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Date, DateTime, ForeignKey, Float
from database import Base
from datetime import datetime

class DiningHall(Base): # Dining hall table
    __tablename__ = "dining_halls" 
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True)

class Item(Base):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    rarity: Mapped[str] = mapped_column(String(50), nullable=True)
    last_seen: Mapped[datetime.date] = mapped_column(Date, nullable=True)

class Appearance(Base):
    __tablename__ = "menu_appearances"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey('items.id'))
    hall_id: Mapped[int] = mapped_column(ForeignKey('dining_halls.id'))
    date: Mapped[datetime.date] = mapped_column(Date)
    food_type: Mapped[str] = mapped_column(String(50), nullable=False)
    calories: Mapped[float] = mapped_column(Float)
    protein: Mapped[float] = mapped_column(Float)
    fat: Mapped[float] = mapped_column(Float, nullable=True)
    carbs: Mapped[float] = mapped_column(Float, nullable=True)