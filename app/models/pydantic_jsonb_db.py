from pydantic import BaseModel
from typing import Optional, Literal 


SkillLevel = Literal["beginner", "intermediate", "advanced", "expert"]
LanguageLevel = Literal["A1", "A2", "B1", "B2", "C1", "Native"]
ResumeLanguage = Literal["EN", "PL"]

class ContactSchema(BaseModel):
    firstName: str
    lastName: str
    email: str
    phone: str
    linkedin: Optional[str] = None
    github: Optional[str] = None
    website: Optional[str] = None
    location: Optional[str] = None


class SkillSchema(BaseModel):
    id: str
    name: str
    level: SkillLevel
    category: Optional[str] = None


class LanguageSchema(BaseModel):
    id: str
    name: str
    level: LanguageLevel


class InterestSchema(BaseModel):
    id: str
    name: str


class ExperienceSchema(BaseModel):
    id: Optional[str] = None
    company: str
    position: str
    startDate: str
    endDate: Optional[str] = None
    current: bool
    description: str
    highlights: Optional[list[str]] = None


class CertificateSchema(BaseModel):
    id: str
    name: str
    issuer: str
    date: str
    expiryDate: Optional[str] = None
    credentialId: Optional[str] = None
    url: Optional[str] = None


class ProjectSchema(BaseModel):
    id: str
    name: str
    description: str
    technologies: list[str]
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    url: Optional[str] = None


class WriterRedefinedTopicSchema(BaseModel):
    redefinedTopic: str
    refinedQuotes: list[str]


class TopicSchema(BaseModel):
    topic: str
    preTopic: WriterRedefinedTopicSchema
