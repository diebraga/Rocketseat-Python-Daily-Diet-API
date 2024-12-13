from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    # Colonnes
    id = Column(Integer, primary_key=True, autoincrement=True)  # ID unique et clé primaire
    username = Column(String(50), unique=True, nullable=False)  # Nom d'utilisateur unique
    password = Column(String(255), nullable=False)             # Mot de passe (idéalement haché)

    # Relation avec Dish
    dishes = relationship("Dish", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"User(id={self.id}, username={self.username})"


    __tablename__ = "dishes"

    # Colonnes
    id = Column(Integer, primary_key=True, autoincrement=True)  # ID unique et clé primaire
    name = Column(String(50), unique=True, nullable=False)      # Nom unique et obligatoire
    description = Column(String(200), nullable=False)           # Limite à 200 caractères
    date_time = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)  # Date/heure en UTC
    is_on_diet = Column(Boolean, nullable=False)                # Indicateur pour régime

    # ForeignKey et relation avec User
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="dishes")

    def __repr__(self):
        return (f"Dish(id={self.id}, name={self.name}, description={self.description}, "
                f"date_time={self.date_time}, is_on_diet={self.is_on_diet}, user_id={self.user_id})")