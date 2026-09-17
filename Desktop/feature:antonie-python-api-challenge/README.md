# Books API - RESTful CRUD Application

A production-ready FastAPI application for managing books and authors using MongoDB. This project includes comprehensive CRUD operations, data relationships, aggregations, Docker containerization, automated testing, and AWS infrastructure as code with Terraform.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Query Parameters](#query-parameters)
- [Database Initialization](#database-initialization)
- [Testing](#testing)
- [Docker](#docker)
- [Infrastructure as Code](#infrastructure-as-code)
- [Architecture](#architecture)

## Features

### Part 1: CRUD Operations (70%)
- ✅ GET `/books/{id}` - Retrieve a specific book
- ✅ GET `/books` - List books with pagination
- ✅ POST `/books` - Create a new book
- ✅ PATCH `/books/{id}` - Update an existing book
- ✅ DELETE `/books/{id}` - Delete a book
- ✅ Input validation using Pydantic
- ✅ Pagination with `page` and `limit` query parameters
- ✅ Proper error handling with HTTP status codes
- ✅ Query parameter filtering (author, title, tags)

### Part 2: Data Relationships & Aggregations (30%)
- ✅ Author schema with id, name, birth_date fields
- ✅ GET `/authors/{author_id}/books` - Retrieve books by specific author
- ✅ GET `/authors` - List authors with book count
- ✅ GET `/publishers/{publisher_name}/average_pages` - Publisher statistics

### Additional Features
- ✅ Comprehensive unit and integration tests with pytest
- ✅ Docker and Docker Compose setup
- ✅ AWS Terraform infrastructure (ECS Fargate, DocumentDB, ALB)
- ✅ CloudWatch monitoring and alarms
- ✅ Health check endpoints
- ✅ API documentation with Swagger/OpenAPI
- ✅ CORS middleware enabled

## Project Structure

```
feature:antonie-python-api-challenge/
├── main.py                          # FastAPI application
├── models.py                        # Pydantic models
├── database.py                      # MongoDB connection & setup
├── test_main.py                     # Unit and integration tests
├── requirements.txt                 # Python dependencies
├── Dockerfile                       # Container image definition
├── docker-compose.yml              # Docker Compose setup
├── README.md                        # This file
└── terraform/                       # AWS Infrastructure as Code
    ├── main.tf                      # Main Terraform configuration
    ├── variables.tf                 # Variable definitions
    ├── outputs.tf                   # Output values
    ├── terraform.tfvars.example    # Example configuration
    └── TERRAFORM_README.md          # Terraform documentation
```

## Prerequisites

- Python 3.11+
- MongoDB 4.0+ (local or Docker)
- Docker & Docker Compose (optional, for containerized setup)
- Terraform (for AWS infrastructure)
- AWS Account (for production deployment)

## Installation

### Local Development Setup

1. **Clone the repository**
   ```bash
   cd feature:antonie-python-api-challenge
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start MongoDB** (if not running locally)
   ```bash
   # Using Docker
   docker run -d -p 27017:27017 --name mongodb mongo:7.0
   
   # Or using Homebrew on macOS
   brew services start mongodb-community
   ```

5. **Set environment variables** (optional)
   ```bash
   # Create .env file
   echo "MONGODB_URI=mongodb://localhost:27017" > .env
   ```

## Running the Application

### Local Development

```bash
# Start the API
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# API will be available at http://localhost:8000
# Swagger UI: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

### Using Docker Compose

```bash
# Start all services (MongoDB + API)
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down

# Remove volumes (data)
docker-compose down -v
```

## API Endpoints

### Books Management

#### 1. Get a Specific Book
```http
GET /books/{id}
```
**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Learning Python",
  "author": "Mark Lutz",
  "publisher": "O'Reilly Media",
  "pages": 1648,
  "tags": ["Python", "Development", "Learning"],
  "created_at": "2017-01-12T00:00:00",
  "updated_at": "2017-01-12T00:00:00"
}
```

#### 2. List All Books
```http
GET /books?page=1&limit=10
```
**Response (200 OK):**
```json
{
  "items": [
    {
      "id": 1,
      "title": "Learning Python",
      "author": "Mark Lutz",
      "publisher": "O'Reilly Media",
      "pages": 1648,
      "tags": ["Python", "Development", "Learning"],
      "created_at": "2017-01-12T00:00:00",
      "updated_at": "2017-01-12T00:00:00"
    }
  ],
  "total": 1,
  "page": 1,
  "limit": 10,
  "pages": 1
}
```

#### 3. Create a New Book
```http
POST /books
Content-Type: application/json

{
  "id": 3,
  "title": "Python Crash Course",
  "author": "Eric Matthes",
  "publisher": "No Starch Press",
  "pages": 544,
  "tags": ["Python", "Beginner", "Learning"]
}
```
**Response (201 Created):**
```json
{
  "id": 3,
  "title": "Python Crash Course",
  "author": "Eric Matthes",
  "publisher": "No Starch Press",
  "pages": 544,
  "tags": ["Python", "Beginner", "Learning"],
  "created_at": "2024-01-16T10:30:00",
  "updated_at": "2024-01-16T10:30:00"
}
```

#### 4. Update a Book
```http
PATCH /books/{id}
Content-Type: application/json

{
  "title": "Learning Python - 5th Edition",
  "pages": 1700
}
```
**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Learning Python - 5th Edition",
  "author": "Mark Lutz",
  "publisher": "O'Reilly Media",
  "pages": 1700,
  "tags": ["Python", "Development", "Learning"],
  "created_at": "2017-01-12T00:00:00",
  "updated_at": "2024-01-16T10:30:00"
}
```

#### 5. Delete a Book
```http
DELETE /books/{id}
```
**Response (204 No Content):**
(Empty response)

### Authors Management

#### 6. Get Books by Author
```http
GET /authors/{author_id}/books
```
**Response (200 OK):**
```json
{
  "author_id": 1,
  "author_name": "Mark Lutz",
  "books": [
    {
      "id": 1,
      "title": "Learning Python",
      "author": "Mark Lutz",
      "publisher": "O'Reilly Media",
      "pages": 1648,
      "tags": ["Python", "Development", "Learning"],
      "created_at": "2017-01-12T00:00:00",
      "updated_at": "2017-01-12T00:00:00"
    }
  ],
  "book_count": 1
}
```

#### 7. List All Authors with Book Count
```http
GET /authors
```
**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Mark Lutz",
    "birth_date": "1959-01-01T00:00:00",
    "book_count": 2
  },
  {
    "id": 2,
    "name": "Harry Percival",
    "birth_date": "1970-01-01T00:00:00",
    "book_count": 1
  }
]
```

#### 8. Get Publisher Statistics
```http
GET /publishers/{publisher_name}/average_pages
```
**Response (200 OK):**
```json
{
  "publisher": "O'Reilly Media",
  "average_pages": 752.0,
  "total_books": 2,
  "max_pages": 1648,
  "min_pages": 304
}
```

### Health & Info

#### 9. Health Check
```http
GET /health
```
**Response (200 OK):**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-16T10:30:00.123456"
}
```

#### 10. API Info
```http
GET /
```
**Response (200 OK):**
```json
{
  "message": "Books API - RESTful CRUD Application",
  "version": "1.0.0",
  "docs": "/docs",
  "openapi": "/openapi.json"
}
```

## Query Parameters

### GET /books - Filtering and Pagination

**Pagination Parameters:**
- `page` (int, default=1): Page number, must be >= 1
- `limit` (int, default=10): Items per page, must be 1-100

**Filter Parameters:**
- `author` (string): Filter by author name (partial match, case-insensitive)
- `title` (string): Filter by book title (partial match, case-insensitive)
- `tags` (string): Filter by tags (comma-separated values)

**Examples:**

```bash
# Get page 2 with 20 items per page
GET /books?page=2&limit=20

# Filter by author
GET /books?author=Mark

# Filter by title
GET /books?title=Python

# Filter by tags (multiple tags)
GET /books?tags=Python,Development

# Combine filters
GET /books?author=Mark&title=Learning&limit=5&page=1
```

## Database Initialization

### Automatic Initialization

The application automatically initializes the database on startup:

1. Connects to MongoDB using the `MONGODB_URI` environment variable
2. Creates collections with proper indexes for:
   - Books: indexed by `id` (unique), `author`, `publisher`
   - Authors: indexed by `id` (unique), `name`
3. Seeds initial data if collections are empty

### Sample Data

The application comes pre-loaded with 2 sample books and 3 sample authors:

**Books:**
```json
[
  {
    "id": 1,
    "title": "Learning Python",
    "author": "Mark Lutz",
    "publisher": "O'Reilly Media",
    "pages": 1648,
    "tags": ["Python", "Development", "Learning"],
    "created_at": "2017-01-12T00:00:00+03:00",
    "updated_at": "2017-01-12T00:00:00+03:00"
  },
  {
    "id": 2,
    "title": "Architecture Patterns with Python",
    "author": "Harry Percival, Bob Gregory",
    "publisher": "O'Reilly Media",
    "pages": 304,
    "tags": ["Python", "Development", "Functional Programming"],
    "created_at": "2017-01-12T00:00:00+03:00",
    "updated_at": "2017-01-12T00:00:00+03:00"
  }
]
```

**Authors:**
```json
[
  {
    "id": 1,
    "name": "Mark Lutz",
    "birth_date": "1959-01-01T00:00:00"
  },
  {
    "id": 2,
    "name": "Harry Percival",
    "birth_date": "1970-01-01T00:00:00"
  },
  {
    "id": 3,
    "name": "Bob Gregory",
    "birth_date": "1975-01-01T00:00:00"
  }
]
```

### MongoDB Connection String

By default, the application connects to:
```
mongodb://localhost:27017
```

To connect to a different MongoDB instance, set the `MONGODB_URI` environment variable:
```bash
export MONGODB_URI="mongodb://username:password@host:port/database_name"
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest test_main.py

# Run specific test class
pytest test_main.py::TestBooksRead

# Run specific test
pytest test_main.py::TestBooksRead::test_get_book_by_id

# Run with coverage report
pytest --cov=. test_main.py
```

### Test Coverage

The test suite includes:

**Part 1 - CRUD Operations (35+ tests):**
- Reading books (get by ID, list with pagination, filters)
- Creating books (valid data, duplicate ID, invalid data)
- Updating books (full update, partial update)
- Deleting books

**Part 2 - Relationships & Aggregations (10+ tests):**
- Getting books by author
- Listing authors with book counts
- Publisher statistics

**Health & Info Endpoints (2 tests):**
- Health check
- Root endpoint

### Test Output Example

```
test_main.py::TestBooksRead::test_get_book_by_id PASSED                  [ 1%]
test_main.py::TestBooksRead::test_get_book_not_found PASSED               [ 2%]
test_main.py::TestBooksRead::test_list_books PASSED                       [ 3%]
test_main.py::TestBooksRead::test_list_books_with_pagination PASSED       [ 4%]
test_main.py::TestBooksRead::test_list_books_filter_by_author PASSED      [ 5%]
...
================================ 47 passed in 1.23s ================================
```

## Docker

### Building the Docker Image

```bash
# Build image
docker build -t books-api:latest .

# Run container
docker run -p 8000:8000 -e MONGODB_URI="mongodb://mongodb:27017" books-api:latest
```

### Using Docker Compose

**Start the stack:**
```bash
docker-compose up -d
```

**Services:**
- **api**: FastAPI application on port 8000
- **mongodb**: MongoDB database on port 27017

**Verify setup:**
```bash
# Check services are running
docker-compose ps

# View API logs
docker-compose logs -f api

# Access API
curl http://localhost:8000/health
```

**Stop and cleanup:**
```bash
# Stop services
docker-compose stop

# Stop and remove containers
docker-compose down

# Stop, remove containers, and delete volumes
docker-compose down -v
```

## Infrastructure as Code

See [terraform/TERRAFORM_README.md](terraform/TERRAFORM_README.md) for detailed information about deploying to AWS.

### Quick Terraform Overview

The Terraform configuration includes:

- **ECS Fargate Cluster** for container orchestration
- **Application Load Balancer** for traffic distribution
- **DocumentDB** for MongoDB-compatible database
- **VPC with Public & Private Subnets** for network isolation
- **Auto-scaling** based on CPU and memory metrics
- **CloudWatch Monitoring** and alarms
- **KMS Encryption** for database security

### Deploying to AWS

```bash
cd terraform

# Copy and customize the configuration
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your values

# Initialize Terraform
terraform init

# Review the plan
terraform plan

# Apply the configuration
terraform apply

# Get outputs (including API URL)
terraform output
```

## Architecture

### Local Development

```
┌─────────────────────────────────────────────────────────────┐
│                      Your Computer                          │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐          ┌──────────────┐                  │
│  │  FastAPI    │◄─────────│  MongoDB     │                  │
│  │  (Port 8000)│          │ (Port 27017) │                  │
│  └──────┬──────┘          └──────────────┘                  │
│         │                                                     │
│   Swagger UI: /docs                                          │
│   ReDoc: /redoc                                              │
└─────────────────────────────────────────────────────────────┘
```

### Docker Compose

```
┌─────────────────────────────────────────────────────────────┐
│                    Docker Compose                            │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐          ┌──────────────────┐          │
│  │   FastAPI        │◄─────────│   MongoDB        │          │
│  │   Container      │          │   Container      │          │
│  │   (Port 8000)    │          │   (Port 27017)   │          │
│  └──────────────────┘          └──────────────────┘          │
│         │                              │                     │
│    books_network (Bridge)              │                     │
└─────────────────────────────────────────────────────────────┘
```

### AWS Deployment

```
┌─────────────────────────────────────────────────────────────┐
│                      AWS Region                             │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐    │
│  │                    VPC (10.0.0.0/16)               │    │
│  │                                                     │    │
│  │  ┌──────────────────────────────────────────┐      │    │
│  │  │     Public Subnets (AZ 1-3)             │      │    │
│  │  │  ┌────────────────────────────────┐     │      │    │
│  │  │  │  Application Load Balancer     │     │      │    │
│  │  │  │  (Port 80 & 443)               │     │      │    │
│  │  │  └────────────┬───────────────────┘     │      │    │
│  │  └───────────────┼─────────────────────────┘      │    │
│  │                  │                                 │    │
│  │  ┌──────────────▼──────────────────────────┐      │    │
│  │  │   Private Subnets (AZ 1-3)             │      │    │
│  │  │                                        │      │    │
│  │  │  ┌─────────────────────────────────┐  │      │    │
│  │  │  │  ECS Fargate Cluster            │  │      │    │
│  │  │  │  ┌─────────────────────────┐    │  │      │    │
│  │  │  │  │ FastAPI Task (2-4)      │    │  │      │    │
│  │  │  │  └─────────────────────────┘    │  │      │    │
│  │  │  └─────────────┬───────────────────┘  │      │    │
│  │  └────────────────┼──────────────────────┘      │    │
│  │                   │                             │    │
│  │  ┌────────────────▼──────────────────────┐      │    │
│  │  │  DocumentDB Cluster                  │      │    │
│  │  │  (MongoDB Compatible)                │      │    │
│  │  │  - 2-3 instances                     │      │    │
│  │  │  - Encrypted at rest                 │      │    │
│  │  │  - Automated backups                 │      │    │
│  │  └───────────────────────────────────────┘      │    │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
│  CloudWatch Logs & Alarms (CPU, Memory, Connections) │
└─────────────────────────────────────────────────────────┘
```

## Error Handling

The API uses standard HTTP status codes:

- **200 OK**: Successful GET request
- **201 Created**: Successful POST request
- **204 No Content**: Successful DELETE request
- **400 Bad Request**: Invalid request parameters (e.g., page exceeds max)
- **404 Not Found**: Resource not found
- **409 Conflict**: Conflict in request (e.g., duplicate ID)
- **422 Unprocessable Entity**: Validation error in request body
- **500 Internal Server Error**: Server error

**Error Response Format:**
```json
{
  "detail": "Error message describing the issue"
}
```

## Performance Considerations

- **Pagination**: Limited to 100 items per page to prevent large dataset transfers
- **Database Indexes**: Created on frequently queried fields (id, author, publisher)
- **Case-insensitive Filtering**: Regex queries with `$options: "i"` for flexibility
- **Aggregation Pipeline**: Used for complex queries like publisher statistics
- **Connection Pooling**: MongoDB connection is managed efficiently
- **Auto-scaling**: ECS auto-scales based on CPU and memory metrics

## Security Considerations

- **Input Validation**: Pydantic models validate all inputs
- **Field Constraints**: String lengths and numeric ranges enforced
- **Encryption**: Database encryption at rest (AWS KMS)
- **Network Isolation**: Private subnets for sensitive components
- **CORS Enabled**: All origins allowed (customize in production)
- **No Sensitive Defaults**: Passwords must be provided

## Troubleshooting

### MongoDB Connection Failed
```
Error: ServerSelectionTimeoutError
```
**Solution**: Ensure MongoDB is running and accessible
```bash
# Check if MongoDB is running
mongo --version

# Start MongoDB if using Homebrew
brew services start mongodb-community

# Or start Docker container
docker run -d -p 27017:27017 mongo:7.0
```

### Port Already in Use
```
Error: Address already in use
```
**Solution**: Use a different port or kill the process
```bash
# Run on different port
uvicorn main:app --port 8001

# Or kill process on port 8000 (macOS/Linux)
lsof -ti:8000 | xargs kill -9
```

### Tests Fail
```
Error: Database collection already exists
```
**Solution**: Tests use mongomock (in-memory DB), so no setup needed
```bash
# Run tests with verbose output
pytest -v

# Check test isolation
pytest --tb=short
```

## Contributing

When contributing to this project:

1. Write tests for new features
2. Follow PEP 8 style guide
3. Update documentation
4. Run `pytest` before submitting

## License

This project is open source and available under the MIT License.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review test cases for usage examples
3. Check FastAPI documentation: https://fastapi.tiangolo.com
4. MongoDB documentation: https://docs.mongodb.com

---

**Version**: 1.0.0  
**Last Updated**: 2024-01-16
