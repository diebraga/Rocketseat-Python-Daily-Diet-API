from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone

Base = declarative_base()

class Dish(Base):
    __tablename__ = "dishes"

    name = Column(String(50), primary_key=True, nullable=False)  # Limite automatique à 50 caractères
    description = Column(String(200), nullable=False)            # Limite automatique à 200 caractères
    date_time = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    is_on_diet = Column(Boolean, nullable=False)

    def __repr__(self):
        return (f"Dish(name={self.name}, description={self.description}, "
                f"date_time={self.date_time}, is_on_diet={self.is_on_diet})")