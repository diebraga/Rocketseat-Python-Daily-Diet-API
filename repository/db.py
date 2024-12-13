from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuration de la base de données
DATABASE_URL = "sqlite:///./database.db"  # Remplacez par votre URL de base de données

# Créer un moteur SQLAlchemy
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Création de la session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Déclarer la base pour les modèles
Base = declarative_base()

# Dépendance pour obtenir une session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()