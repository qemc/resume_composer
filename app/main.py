from app.config.database import with_session_query
from sqlalchemy.orm import sessionmaker
from app.models.models import Experiences
from fastapi import FastAPI

app = FastAPI()

@with_session_query
def get_user_by_id(session: sessionmaker, user_id: int) -> Experiences:
    return session.get(Experiences, user_id)


if __name__ == "__main__":

    exp: Experiences = get_user_by_id(1)
    if exp:
        print(f"Found user: {exp.experience.company}")
    else:
        print("User not found")



# To do:
# Add pydantic models for database json blobs - done
# Unify way of quering data from database (factory?) - done (wrapers)


# Draft agentic logic 
# Set up easy fastAPI server