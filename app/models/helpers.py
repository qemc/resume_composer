from typing import Type, Any
from sqlalchemy.types import TypeDecorator
from sqlalchemy.dialects.postgresql import JSONB
from pydantic import BaseModel


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