from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from repository.database import Base

class Dish(Base):
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(200), nullable=False)
    date_time = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    is_on_diet = Column(Boolean, nullable=False)

    # ForeignKey vers User
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="dishes")

    def __repr__(self):
        return (f"Dish(id={self.id}, name={self.name}, description={self.description}, "
                f"date_time={self.date_time}, is_on_diet={self.is_on_diet}, user_id={self.user_id})")