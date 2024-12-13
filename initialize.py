from sqlalchemy.orm import Session
from repository.database import Base, engine  # Importer Base et engine depuis db
from models.dish import Dish  # Assurez-vous que les modèles sont importés ici
from models.user import User
import bcrypt

def initialize():
    # Créer les tables s'il n'existe pas déjà
    Base.metadata.create_all(bind=engine)
    print("Tables créées ou déjà existantes.")

    session = Session(bind=engine)

    # Vérifier si l'utilisateur admin existe déjà
    admin_user = session.query(User).filter_by(username="admin").first()
    if not admin_user:
        hashed_password = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt())
        admin_user = User(
            username="admin",
            password=hashed_password.decode('utf-8'),
            is_admin=True
        )
        session.add(admin_user)
        session.commit()
        print("Utilisateur admin créé avec succès.")
    else:
        print("Utilisateur admin déjà existant.")

    session.close()

if __name__ == "__main__":
    initialize()