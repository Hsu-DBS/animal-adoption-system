from app.db.database import SessionLocal, engine, Base
from app.models.user import User
from app.models.enums import UserType
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_first_admin():

    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if admin already exists
        existing_admin = db.query(User).filter(User.user_type == UserType.Admin).first()
        
        if existing_admin:
            print(f"Admin '{existing_admin.name}' already exists!")
            return
        
        # Create first admin
        admin = User(
            name="Admin",
            email="admin@gmail.com",
            password=pwd_context.hash("Admin@123"),
            phone="09971257432",
            address="Yangon Animal Shelter",
            user_type=UserType.Admin,
            created_by="System"
        )
        
        db.add(admin)
        db.commit()
        db.refresh(admin)
        
    except Exception as e:
        print(e)
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_first_admin()