"""
Pydantic models for data validation.

References:
- Pydantic Docs: https://docs.pydantic.dev/latest/
- Field Validation: https://docs.pydantic.dev/latest/api/fields/
- BaseModel: https://docs.pydantic.dev/latest/api/main/#pydantic.BaseModel
"""

from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class BookBase(BaseModel):
    """Base book model with common fields"""
    title: str = Field(..., min_length=1, max_length=255)
    author: str = Field(..., min_length=1, max_length=255)
    publisher: str = Field(..., min_length=1, max_length=255)
    pages: int = Field(..., ge=1, description="Must be at least 1 page")
    tags: list[str] = Field(default_factory=list)
    
    @field_validator("pages")
    @classmethod
    def validate_pages(cls, v: int) -> int:
        """Validate pages is positive integer. See: https://docs.pydantic.dev/latest/api/functional_validators/"""
        if v < 1:
            raise ValueError("Pages must be at least 1")
        return v


class BookCreate(BookBase):
    """Model for creating a new book"""
    id: int = Field(..., ge=1, description="Unique book ID")
    created_at: datetime | None = None
    updated_at: datetime | None = None


class BookUpdate(BaseModel):
    """Model for updating an existing book. All fields optional."""
    title: str | None = Field(None, min_length=1, max_length=255)
    author: str | None = Field(None, min_length=1, max_length=255)
    publisher: str | None = Field(None, min_length=1, max_length=255)
    pages: int | None = Field(None, ge=1)
    tags: list[str] | None = None


class Book(BookBase):
    """Complete book response model"""
    id: int = Field(..., ge=1)
    created_at: datetime
    updated_at: datetime


class AuthorBase(BaseModel):
    """Base author model"""
    name: str = Field(..., min_length=1, max_length=255)
    birth_date: datetime | None = None


class AuthorCreate(AuthorBase):
    """Model for creating a new author"""
    id: int = Field(..., ge=1, description="Unique author ID")


class AuthorUpdate(BaseModel):
    """Model for updating an existing author"""
    name: str | None = Field(None, min_length=1, max_length=255)
    birth_date: datetime | None = None


class Author(AuthorBase):
    """Complete author response model"""
    id: int = Field(..., ge=1)


class AuthorWithBookCount(Author):
    """Author model with book count aggregation"""
    book_count: int = Field(..., ge=0, description="Total books by this author")
