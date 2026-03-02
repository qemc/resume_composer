from datetime import datetime
from pydantic import BaseModel, HttpUrl

class JobOfferResponse(BaseModel):
    status: str
    initial_url: HttpUrl
    url: HttpUrl
    title: str
    company: str
    source: str
    location: str
    salary: str
    experience_level: str
    employment_type: str
    work_mode: str
    description: str
    scraped_at: datetime