"""
Database module for MongoDB connection and initialization.

References:
- PyMongo Docs: https://pymongo.readthedocs.io/
- Connection String: https://docs.mongodb.com/manual/reference/connection-string/
- Indexing: https://docs.mongodb.com/manual/indexes/
- Error Handling: https://pymongo.readthedocs.io/en/stable/api/pymongo/errors.html
"""

import os
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure
from datetime import datetime

# Global database instance
_db: Database | None = None
_client: MongoClient | None = None

SAMPLE_AUTHORS = [
    {"id": 1, "name": "Mark Lutz", "birth_date": "1959-01-01T00:00:00"},
    {"id": 2, "name": "Harry Percival", "birth_date": "1970-01-01T00:00:00"},
    {"id": 3, "name": "Bob Gregory", "birth_date": "1975-01-01T00:00:00"},
]

SAMPLE_BOOKS = [
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
]


def init_db(uri: str | None = None) -> Database:
    """
    Initialize MongoDB connection and seed data.
    
    Uses connection pooling with retry logic.
    See: https://pymongo.readthedocs.io/en/stable/examples/connection_pooling.html
    
    Args:
        uri: MongoDB connection string. Defaults to MONGODB_URI env or localhost
    
    Returns:
        Database: MongoDB database instance
    
    Raises:
        ServerSelectionTimeoutError: If MongoDB connection fails
    """
    global _db, _client
    
    uri = uri or os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    
    try:
        # Create MongoClient with connection pooling and retry settings
        # Ref: https://pymongo.readthedocs.io/en/stable/api/pymongo/mongo_client.html
        _client = MongoClient(
            uri,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=10000,
            retryWrites=True,
            maxPoolSize=50,
            minPoolSize=10
        )
        
        _db = _client.get_database("books_db")
        
        # Verify connection with ping command
        # Ref: https://docs.mongodb.com/manual/reference/command/ping/
        _client.admin.command("ping")
        print("✓ MongoDB connected successfully")
        
        # Create indexes for optimal query performance
        # Ref: https://docs.mongodb.com/manual/indexes/
        _db.books.create_index("id", unique=True)
        _db.books.create_index("author")
        _db.books.create_index("publisher")
        _db.authors.create_index("id", unique=True)
        _db.authors.create_index("name")
        print("✓ Database indexes created")
        
        # Seed data if collections are empty
        if _db.books.count_documents({}) == 0:
            _db.authors.insert_many(SAMPLE_AUTHORS)
            _db.books.insert_many(SAMPLE_BOOKS)
            print("✓ Sample data seeded")
        
        return _db
    
    except (ServerSelectionTimeoutError, ConnectionFailure) as e:
        print(f"✗ MongoDB connection failed: {e}")
        raise


def get_database() -> Database:
    """
    Get database instance. Initializes on first call.
    
    Returns:
        Database: MongoDB database instance
    """
    global _db
    if _db is None:
        init_db()
    return _db


def close_db() -> None:
    """
    Close database connection gracefully.
    
    See: https://pymongo.readthedocs.io/en/stable/api/pymongo/mongo_client.html#pymongo.MongoClient.close
    """
    global _client
    if _client:
        _client.close()
        print("✓ MongoDB connection closed")
