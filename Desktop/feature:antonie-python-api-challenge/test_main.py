"""
Unit and integration tests for Books API.

References:
- Pytest: https://docs.pytest.org/
- FastAPI Testing: https://fastapi.tiangolo.com/advanced/testing-dependencies/
- mongomock: https://github.com/mongomock/mongomock
- HTTP Status Codes: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status

Test Coverage:
- CRUD operations (Create, Read, Update, Delete)
- Query filtering and pagination
- Author management and aggregations
- Error handling and validation
- Health endpoints
"""

import pytest
from fastapi.testclient import TestClient
from mongomock import MongoClient
from datetime import datetime

from main import app
from database import get_database


@pytest.fixture(autouse=True)
def mock_db(monkeypatch):
    """
    Create mock MongoDB for testing using mongomock.
    
    This fixture:
    - Creates an in-memory MongoDB instance (no external DB needed)
    - Seeds test data automatically
    - Cleans up after each test
    
    Ref: https://github.com/mongomock/mongomock
    """
    client = MongoClient()
    test_db = client.get_database("test_books_db")
    
    # Patch get_database to use mock
    monkeypatch.setattr("main.get_database", lambda: test_db)
    
    # Seed test data
    test_db.authors.insert_many([
        {"id": 1, "name": "Mark Lutz", "birth_date": "1959-01-01T00:00:00"},
        {"id": 2, "name": "Harry Percival", "birth_date": "1970-01-01T00:00:00"},
        {"id": 3, "name": "Bob Gregory", "birth_date": "1975-01-01T00:00:00"},
    ])
    
    test_db.books.insert_many([
        {
            "id": 1,
            "title": "Learning Python",
            "publisher": "O'Reilly Media",
            "author": "Mark Lutz",
            "pages": 1648,
            "created_at": datetime.fromisoformat("2017-01-12T00:00:00"),
            "tags": ["Python", "Development", "Learning"],
            "updated_at": datetime.fromisoformat("2017-01-12T00:00:00"),
        },
        {
            "id": 2,
            "title": "Architecture Patterns with Python",
            "publisher": "O'Reilly Media",
            "author": "Harry Percival, Bob Gregory",
            "pages": 304,
            "tags": ["Python", "Development", "Functional Programming"],
            "created_at": datetime.fromisoformat("2017-01-12T00:00:00"),
            "updated_at": datetime.fromisoformat("2017-01-12T00:00:00"),
        },
        {
            "id": 3,
            "title": "Fluent Python",
            "publisher": "O'Reilly Media",
            "author": "Mark Lutz",
            "pages": 792,
            "tags": ["Python", "Development"],
            "created_at": datetime.fromisoformat("2015-08-01T00:00:00"),
            "updated_at": datetime.fromisoformat("2015-08-01T00:00:00"),
        },
    ])
    
    yield test_db
    
    # Cleanup
    client.drop_database("test_books_db")


@pytest.fixture
def client():
    """
    Create TestClient for FastAPI testing.
    
    Ref: https://fastapi.tiangolo.com/advanced/testing-dependencies/
    """
    return TestClient(app)


class TestBooksRead:
    """Tests for reading books (GET operations).
    
    Ref: https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/GET
    """
    
    def test_get_book_by_id(self, client):
        """Test GET /books/{id} returns correct book"""
        response = client.get("/books/1")
        assert response.status_code == 200
        assert response.json()["id"] == 1
        assert response.json()["title"] == "Learning Python"
    
    def test_get_book_not_found(self, client):
        """Test GET /books/{id} returns 404 for non-existent book"""
        response = client.get("/books/999")
        assert response.status_code == 404
    
    def test_list_books(self, client):
        """Test GET /books returns paginated list"""
        response = client.get("/books")
        assert response.status_code == 200
        data = response.json()
        assert all(k in data for k in ["items", "total", "page", "limit", "pages"])
        assert len(data["items"]) >= 1
    
    @pytest.mark.parametrize("page,limit", [(1, 2), (2, 1), (1, 10)])
    def test_list_books_pagination(self, client, page, limit):
        """Test pagination with different page and limit values"""
        response = client.get(f"/books?page={page}&limit={limit}")
        assert response.status_code == 200
        assert response.json()["page"] == page
        assert response.json()["limit"] == limit
    
    @pytest.mark.parametrize("filter_type,value,field", [
        ("author", "Mark", "author"),
        ("title", "Python", "title"),
    ])
    def test_list_books_filter(self, client, filter_type, value, field):
        """Test text filtering for author and title (case-insensitive)"""
        response = client.get(f"/books?{filter_type}={value}")
        assert response.status_code == 200
        data = response.json()
        assert all(value.lower() in item[field].lower() for item in data["items"])
    
    def test_list_books_filter_tags(self, client):
        """Test tag filtering (any tag match)"""
        response = client.get("/books?tags=Development")
        assert response.status_code == 200
        assert all("Development" in item["tags"] for item in response.json()["items"])


class TestBooksWrite:
    """Tests for writing books (POST, PATCH, DELETE operations).
    
    Ref: https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST
    Ref: https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PATCH
    Ref: https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/DELETE
    """
    
    def test_create_book(self, client):
        """Test POST /books creates book with 201 status"""
        response = client.post("/books", json={
            "id": 100,
            "title": "Test Book",
            "author": "Test Author",
            "publisher": "Test Publisher",
            "pages": 300,
            "tags": ["test"],
        })
        assert response.status_code == 201
        assert response.json()["id"] == 100
    
    def test_create_book_duplicate_id(self, client):
        """Test POST /books returns 409 for duplicate ID"""
        response = client.post("/books", json={
            "id": 1,
            "title": "Duplicate",
            "author": "Author",
            "publisher": "Publisher",
            "pages": 100,
        })
        assert response.status_code == 409
    
    @pytest.mark.parametrize("invalid_data", [
        {"id": 101, "title": "", "author": "A", "publisher": "P", "pages": 1},
        {"id": 101, "title": "T", "author": "A", "publisher": "P", "pages": -1},
    ])
    def test_create_book_invalid(self, client, invalid_data):
        """Test POST /books returns 422 for invalid data"""
        response = client.post("/books", json=invalid_data)
        assert response.status_code == 422
    
    def test_update_book(self, client):
        """Test PATCH /books/{id} updates specific fields"""
        response = client.patch("/books/1", json={
            "title": "Updated Title",
            "pages": 2000
        })
        assert response.status_code == 200
        assert response.json()["title"] == "Updated Title"
        assert response.json()["pages"] == 2000
        assert response.json()["author"] == "Mark Lutz"
    
    def test_update_book_not_found(self, client):
        """Test PATCH /books/{id} returns 404 for non-existent book"""
        response = client.patch("/books/999", json={"title": "Updated"})
        assert response.status_code == 404
    
    def test_delete_book(self, client):
        """Test DELETE /books/{id} removes book"""
        response = client.delete("/books/1")
        assert response.status_code == 204
        
        # Verify deleted
        get_response = client.get("/books/1")
        assert get_response.status_code == 404
    
    def test_delete_book_not_found(self, client):
        """Test DELETE /books/{id} returns 404 for non-existent book"""
        response = client.delete("/books/999")
        assert response.status_code == 404


class TestAuthors:
    """Tests for author endpoints and relationships.
    
    Tests author aggregation and book relationships.
    """
    
    def test_get_books_by_author(self, client):
        """Test GET /authors/{id}/books returns all books by author"""
        response = client.get("/authors/1/books")
        assert response.status_code == 200
        data = response.json()
        assert data["author_id"] == 1
        assert data["author_name"] == "Mark Lutz"
        assert data["book_count"] >= 1
    
    def test_get_books_by_author_not_found(self, client):
        """Test GET /authors/{id}/books returns 404 for non-existent author"""
        response = client.get("/authors/999/books")
        assert response.status_code == 404
    
    def test_list_authors(self, client):
        """Test GET /authors returns all authors with book counts"""
        response = client.get("/authors")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert all("book_count" in author for author in data)
    
    def test_list_authors_book_count(self, client):
        """Test book count aggregation is accurate"""
        response = client.get("/authors")
        authors = response.json()
        mark = next(a for a in authors if a["name"] == "Mark Lutz")
        assert mark["book_count"] >= 2


class TestPublishers:
    """Tests for publisher aggregation endpoints.
    
    Uses MongoDB aggregation pipeline for statistics.
    Ref: https://docs.mongodb.com/manual/aggregation/
    """
    
    def test_get_publisher_stats(self, client):
        """Test GET /publishers/{name}/average_pages returns statistics"""
        response = client.get("/publishers/O'Reilly Media/average_pages")
        assert response.status_code == 200
        data = response.json()
        assert all(k in data for k in ["publisher", "average_pages", "total_books", "max_pages", "min_pages"])
        assert data["total_books"] >= 1
    
    def test_get_publisher_not_found(self, client):
        """Test GET /publishers/{name}/average_pages returns 404 for non-existent publisher"""
        response = client.get("/publishers/NonExistent/average_pages")
        assert response.status_code == 404


class TestHealth:
    """Tests for health and info endpoints."""
    
    def test_health_check(self, client):
        """Test GET /health returns healthy status"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_root(self, client):
        """Test GET / returns API information"""
        response = client.get("/")
        assert response.status_code == 200
        assert "version" in response.json()
