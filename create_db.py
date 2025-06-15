from database import Base, engine
import models  # علشان يتعرف على الكلاسات كلها

def create_database():
    Base.metadata.create_all(bind=engine)
    print("✅ Database and tables created successfully.")

if __name__ == "__main__":
    create_database()
