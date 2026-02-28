from pydantic import BaseModel
from typing import Optional, Literal, Type, Any
from sqlalchemy.types import TypeDecorator
from sqlalchemy.dialects.postgresql import JSONB



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



class PydanticJSONBridge(TypeDecorator):

    impl = JSONB
    cache_ok = True

    def __init__(self, pydantic_model: Type[BaseModel], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pydantic_model = pydantic_model

    def process_bind_param(self, value: Any, dialect) -> dict | None:
        """Going IN to the Database"""
        if value is None:
            return None
        
        if isinstance(value, self.pydantic_model):
            return value.model_dump(mode='json')
            
        if isinstance(value, dict):
            return self.pydantic_model.model_validate(value).model_dump(mode='json')
            
        raise ValueError(f"Expected {self.pydantic_model.__name__} or dict, got {type(value)}")


    def process_result_value(self, value: dict | None, dialect) -> BaseModel | None:
        """Coming OUT of the Database"""
        if value is None:
            return None
            
        return self.pydantic_model.model_validate(value)