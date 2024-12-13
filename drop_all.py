from repository.database import engine, Base

def drop_all_tables():
    # Supprimer toutes les tables
    Base.metadata.drop_all(bind=engine)
    print("Toutes les tables ont été supprimées.")

if __name__ == "__main__":
    drop_all_tables()