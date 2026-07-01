from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Date, DateTime, ForeignKey, Float, func
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

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    profile_picture: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

class Rating(Base):
    __tablename__ = "ratings"
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey('items.id'), primary_key=True)
    score: Mapped[int] = mapped_column(Integer())
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())