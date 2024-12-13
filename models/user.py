from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.orm import relationship
from repository.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)

    # Utilisez une chaîne pour différer la résolution de la relation
    dishes = relationship("Dish", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, is_admin={self.is_admin})"