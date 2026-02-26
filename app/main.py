from app.config.database import SessionLocal
from app.models.models import Users



def get_user_by_id(user_id: int):
    
    with SessionLocal() as session:
        user = session.get(Users, user_id)
        return user



if __name__ == "__main__":

    user = get_user_by_id(2)
    if user:
        print(f"Found user: {user.email}")
    else:
        print("User not found")



# To do:
# Add pydantic models for database json blobs
# Clean code gen models to keep only those used by Agents
# Unify way of quering data from database (factory?)