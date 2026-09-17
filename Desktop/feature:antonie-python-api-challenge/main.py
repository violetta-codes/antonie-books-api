"""
FastAPI application for Books Management.

This module implements a RESTful CRUD API with MongoDB backend.

References:
- FastAPI: https://fastapi.tiangolo.com/
- Async/Await: https://fastapi.tiangolo.com/async-sql-databases/
- Status Codes: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
- MongoDB Regex: https://docs.mongodb.com/manual/reference/operator/query/regex/
- MongoDB Aggregation: https://docs.mongodb.com/manual/aggregation/
- CORS: https://fastapi.tiangolo.com/tutorial/cors/
"""

from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pymongo.database import Database
from pymongo.errors import DuplicateKeyError, OperationFailure
from datetime import datetime
from math import ceil

from models import Book, BookCreate, BookUpdate
from database import init_db, close_db, get_database


def build_filter_query(
    author: str | None, title: str | None, tags: str | None
) -> dict:
    """
    Build MongoDB filter query from search parameters.
    
    Uses regex for text search (case-insensitive) and $in for tag matching.
    Ref: https://docs.mongodb.com/manual/reference/operator/query/regex/
    
    Args:
        author: Author name partial match
        title: Book title partial match
        tags: Comma-separated tags (any match)
    
    Returns:
        dict: MongoDB query filter
    """
    query = {}
    if author:
        query["author"] = {"$regex": author, "$options": "i"}
    if title:
        query["title"] = {"$regex": title, "$options": "i"}
    if tags:
        tag_list = [t.strip() for t in tags.split(",")]
        query["tags"] = {"$in": tag_list}
    return query


def paginate(collection, filter_query: dict, page: int, limit: int) -> dict:
    """
    Paginate MongoDB collection results.
    
    Ref: https://docs.mongodb.com/manual/reference/method/cursor.skip/
    
    Args:
        collection: MongoDB collection
        filter_query: MongoDB query filter
        page: Page number (1-indexed)
        limit: Items per page
    
    Returns:
        dict: Paginated results with metadata
    
    Raises:
        HTTPException: If page exceeds total pages
    """
    total = collection.count_documents(filter_query)
    pages = ceil(total / limit) if total > 0 else 0
    
    if page > pages and total > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Page {page} exceeds max pages {pages}"
        )
    
    skip = (page - 1) * limit
    items = list(collection.find(filter_query).skip(skip).limit(limit))
    
    # Remove MongoDB's internal _id field
    for item in items:
        item.pop("_id", None)
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": pages
    }


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan context manager for startup/shutdown events.
    
    Ref: https://fastapi.tiangolo.com/advanced/events/#alternative-events-deprecated
    """
    # Startup
    init_db()
    yield
    # Shutdown
    close_db()


app = FastAPI(
    title="Books API",
    description="RESTful CRUD API for managing books and authors using FastAPI and MongoDB",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    openapi_url="/openapi.json",
)

# Add CORS middleware
# Ref: https://fastapi.tiangolo.com/tutorial/cors/
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# BOOKS ENDPOINTS
# ============================================================================

@app.get("/books/{book_id}", response_model=Book, tags=["Books"])
async def get_book(book_id: int):
    """
    Retrieve a specific book by ID.
    
    HTTP Status Codes:
    - 200 OK: Book found
    - 404 NOT FOUND: Book doesn't exist
    
    Ref: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/200
    """
    db: Database = get_database()
    book = db.books.find_one({"id": book_id})
    
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )
    
    book.pop("_id", None)
    return book


@app.get("/books", tags=["Books"])
async def list_books(
    page: int = Query(1, ge=1, description="Page number starting from 1"),
    limit: int = Query(10, ge=1, le=100, description="Results per page (1-100)"),
    author: str | None = Query(None, description="Filter by author name (partial match)"),
    title: str | None = Query(None, description="Filter by book title (partial match)"),
    tags: str | None = Query(None, description="Filter by tags (comma-separated)")
) -> dict:
    """
    List books with pagination and filtering.
    
    Query Parameters:
    - page: Page number (default 1)
    - limit: Items per page, max 100 (default 10)
    - author: Filter by author (case-insensitive)
    - title: Filter by title (case-insensitive)
    - tags: Filter by tags (comma-separated)
    
    Example: /books?author=Mark&limit=5&page=1
    
    HTTP Status Codes:
    - 200 OK: Success
    - 400 BAD REQUEST: Invalid page number
    
    Ref: https://docs.mongodb.com/manual/reference/operator/query/regex/
    """
    db: Database = get_database()
    filter_query = build_filter_query(author, title, tags)
    return paginate(db.books, filter_query, page, limit)


@app.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED, tags=["Books"])
async def create_book(book: BookCreate):
    """
    Create a new book.
    
    HTTP Status Codes:
    - 201 CREATED: Book created successfully
    - 409 CONFLICT: Book ID already exists
    - 422 UNPROCESSABLE ENTITY: Validation error
    
    Ref: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/201
    """
    db: Database = get_database()
    
    if db.books.find_one({"id": book.id}):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Book with ID {book.id} already exists"
        )
    
    book_dict = book.dict()
    book_dict["created_at"] = book_dict.get("created_at") or datetime.utcnow()
    book_dict["updated_at"] = book_dict.get("updated_at") or datetime.utcnow()
    
    try:
        result = db.books.insert_one(book_dict)
        created = db.books.find_one({"_id": result.inserted_id})
        created.pop("_id", None)
        return created
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create book: {str(e)}"
        )


@app.patch("/books/{book_id}", response_model=Book, tags=["Books"])
async def update_book(book_id: int, book_update: BookUpdate):
    """
    Update an existing book (partial update).
    
    Only provided fields are updated. Other fields remain unchanged.
    
    HTTP Status Codes:
    - 200 OK: Book updated successfully
    - 404 NOT FOUND: Book doesn't exist
    - 422 UNPROCESSABLE ENTITY: Validation error
    
    Ref: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/200
    """
    db: Database = get_database()
    
    if not db.books.find_one({"id": book_id}):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )
    
    update_data = book_update.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    
    try:
        db.books.update_one({"id": book_id}, {"$set": update_data})
        updated = db.books.find_one({"id": book_id})
        updated.pop("_id", None)
        return updated
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update book: {str(e)}"
        )


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Books"])
async def delete_book(book_id: int):
    """
    Delete a book by ID.
    
    HTTP Status Codes:
    - 204 NO CONTENT: Book deleted successfully
    - 404 NOT FOUND: Book doesn't exist
    
    Ref: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/204
    """
    db: Database = get_database()
    result = db.books.delete_one({"id": book_id})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )


# ============================================================================
# AUTHORS ENDPOINTS
# ============================================================================

@app.get("/authors/{author_id}/books", tags=["Authors"])
async def get_books_by_author(author_id: int):
    """
    Retrieve all books written by a specific author.
    
    HTTP Status Codes:
    - 200 OK: Success
    - 404 NOT FOUND: Author doesn't exist
    """
    db: Database = get_database()
    author = db.authors.find_one({"id": author_id})
    
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Author with ID {author_id} not found"
        )
    
    books = list(db.books.find({"author": author["name"]}))
    for book in books:
        book.pop("_id", None)
    
    return {
        "author_id": author_id,
        "author_name": author["name"],
        "books": books,
        "book_count": len(books)
    }


@app.get("/authors", tags=["Authors"])
async def list_authors():
    """
    List all authors with book count aggregation.
    
    Uses MongoDB aggregation to count books per author.
    
    Returns:
        list: Authors with book counts
    
    Ref: https://docs.mongodb.com/manual/aggregation/
    """
    db: Database = get_database()
    authors = list(db.authors.find())
    
    result = []
    for author in authors:
        author.pop("_id", None)
        book_count = db.books.count_documents({"author": author["name"]})
        result.append({**author, "book_count": book_count})
    
    return result


@app.get("/publishers/{publisher_name}/average_pages", tags=["Publishers"])
async def get_publisher_stats(publisher_name: str):
    """
    Get publisher statistics including average pages.
    
    Uses MongoDB aggregation pipeline for statistics calculation.
    
    HTTP Status Codes:
    - 200 OK: Success
    - 404 NOT FOUND: Publisher not found
    
    Ref: https://docs.mongodb.com/manual/reference/operator/aggregation/group/
    """
    db: Database = get_database()
    
    # MongoDB aggregation pipeline
    # Ref: https://docs.mongodb.com/manual/core/aggregation-pipeline/
    pipeline = [
        {"$match": {"publisher": {"$regex": publisher_name, "$options": "i"}}},
        {
            "$group": {
                "_id": "$publisher",
                "average_pages": {"$avg": "$pages"},
                "total_books": {"$sum": 1},
                "max_pages": {"$max": "$pages"},
                "min_pages": {"$min": "$pages"}
            }
        }
    ]
    
    try:
        result = list(db.books.aggregate(pipeline))
    except OperationFailure as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Aggregation failed: {str(e)}"
        )
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No books found for publisher '{publisher_name}'"
        )
    
    stats = result[0]
    return {
        "publisher": stats["_id"],
        "average_pages": round(stats["average_pages"], 2),
        "total_books": stats["total_books"],
        "max_pages": stats["max_pages"],
        "min_pages": stats["min_pages"]
    }


# ============================================================================
# HEALTH & INFO ENDPOINTS
# ============================================================================

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint for monitoring.
    
    Returns service status and timestamp.
    Useful for load balancers and health monitoring.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "Books API v1.0.0"
    }


@app.get("/", tags=["Root"])
async def root():
    """API root endpoint with service information."""
    return {
        "message": "Books API - RESTful CRUD Application",
        "version": "1.0.0",
        "docs": "/docs",
        "openapi": "/openapi.json",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    # Ref: https://www.uvicorn.org/
    uvicorn.run(app, host="0.0.0.0", port=8000)
