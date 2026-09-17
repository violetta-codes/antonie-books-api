# Technical References & Documentation

This document provides references to all external libraries, frameworks, and best practices used in the Books API.

## Framework & Web

### FastAPI
- **Documentation**: https://fastapi.tiangolo.com/
- **Used For**: RESTful API framework with automatic API documentation
- **Key Features Used**:
  - Async/await support
  - Automatic request validation
  - OpenAPI schema generation
  - Dependency injection
  
**Key Docs**:
- Async: https://fastapi.tiangolo.com/async-sql-databases/
- Testing: https://fastapi.tiangolo.com/advanced/testing-dependencies/
- CORS: https://fastapi.tiangolo.com/tutorial/cors/
- Lifespan: https://fastapi.tiangolo.com/advanced/events/

### Uvicorn
- **Documentation**: https://www.uvicorn.org/
- **Used For**: ASGI server to run FastAPI application
- **Usage**: `uvicorn main:app --host 0.0.0.0 --port 8000`

---

## Data Validation & Models

### Pydantic v2
- **Documentation**: https://docs.pydantic.dev/latest/
- **Used For**: Data validation and parsing
- **Key Features Used**:
  - `BaseModel` for data schemas
  - Field validation with `Field()`
  - `field_validator` for custom validation
  - Type hints for auto-validation

**Key Docs**:
- BaseModel: https://docs.pydantic.dev/latest/api/main/#pydantic.BaseModel
- Fields: https://docs.pydantic.dev/latest/api/fields/
- Validators: https://docs.pydantic.dev/latest/api/functional_validators/

---

## Database

### PyMongo
- **Documentation**: https://pymongo.readthedocs.io/
- **Used For**: MongoDB driver for Python
- **Key Features Used**:
  - Connection pooling
  - Async operations
  - Bulk operations
  - Index creation

**Key Docs**:
- Connection Pooling: https://pymongo.readthedocs.io/en/stable/examples/connection_pooling.html
- MongoClient: https://pymongo.readthedocs.io/en/stable/api/pymongo/mongo_client.html
- Error Handling: https://pymongo.readthedocs.io/en/stable/api/pymongo/errors.html
- Database API: https://pymongo.readthedocs.io/en/stable/api/pymongo/database.html

### MongoDB
- **Documentation**: https://docs.mongodb.com/
- **Used For**: NoSQL database for data persistence
- **Key Features Used**:
  - Collections and documents
  - Indexes for query optimization
  - Aggregation pipeline for complex queries
  - Regex queries for text search

**Key Docs**:
- Connection String: https://docs.mongodb.com/manual/reference/connection-string/
- Indexes: https://docs.mongodb.com/manual/indexes/
- Aggregation Pipeline: https://docs.mongodb.com/manual/aggregation/
- Aggregation Operators:
  - $match: https://docs.mongodb.com/manual/reference/operator/aggregation/match/
  - $group: https://docs.mongodb.com/manual/reference/operator/aggregation/group/
  - $avg: https://docs.mongodb.com/manual/reference/operator/aggregation/avg/
- Query Operators:
  - $regex: https://docs.mongodb.com/manual/reference/operator/query/regex/
  - $in: https://docs.mongodb.com/manual/reference/operator/query/in/
- Ping Command: https://docs.mongodb.com/manual/reference/command/ping/

---

## Testing

### Pytest
- **Documentation**: https://docs.pytest.org/
- **Used For**: Unit and integration testing framework
- **Key Features Used**:
  - Test fixtures (`@pytest.fixture`)
  - Parametrized tests (`@pytest.mark.parametrize`)
  - Monkeypatching for mocking
  - Test discovery and execution

**Key Docs**:
- Fixtures: https://docs.pytest.org/latest/how-to/fixtures.html
- Parametrize: https://docs.pytest.org/latest/how-to/parametrize.html
- Monkeypatch: https://docs.pytest.org/latest/how-to/monkeypatch.html

### mongomock
- **Documentation**: https://github.com/mongomock/mongomock
- **Used For**: In-memory MongoDB mock for testing (no external DB needed)
- **Benefits**:
  - Fast test execution
  - No MongoDB installation required
  - Automatic cleanup between tests

---

## HTTP Standards

### HTTP Status Codes
- **Reference**: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
- **Used Codes**:
  - `200 OK`: Successful GET/PATCH
  - `201 Created`: Successful POST
  - `204 No Content`: Successful DELETE
  - `400 Bad Request`: Invalid parameters
  - `404 Not Found`: Resource doesn't exist
  - `409 Conflict`: Duplicate resource
  - `422 Unprocessable Entity`: Validation error
  - `500 Internal Server Error`: Server error

### HTTP Methods
- **Reference**: https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods
- **Used Methods**:
  - GET: https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/GET
  - POST: https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST
  - PATCH: https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PATCH
  - DELETE: https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/DELETE

### REST Principles
- **Reference**: https://en.wikipedia.org/wiki/Representational_state_transfer
- **Key Concepts**:
  - Resource-based URLs
  - HTTP methods for operations
  - Stateless communication
  - JSON for data exchange

---

## Infrastructure & Deployment

### Docker
- **Documentation**: https://docs.docker.com/
- **Used For**: Containerization of application and database
- **Files**:
  - `Dockerfile`: Application container image
  - `docker-compose.yml`: Multi-container orchestration

**Key Docs**:
- Dockerfile Reference: https://docs.docker.com/engine/reference/builder/
- Docker Compose: https://docs.docker.com/compose/

### AWS Services (Terraform)
- **Terraform Documentation**: https://www.terraform.io/docs/

**AWS Services Used**:
- **ECS Fargate**: Container orchestration (no server management)
  - Docs: https://docs.aws.amazon.com/ecs/latest/developerguide/launch_types.html
  - Auto-scaling: https://docs.aws.amazon.com/autoscaling/application/userguide/application-auto-scaling-target-tracking.html

- **Application Load Balancer (ALB)**: Traffic distribution
  - Docs: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/

- **DocumentDB**: MongoDB-compatible database service
  - Docs: https://docs.aws.amazon.com/documentdb/latest/developerguide/

- **VPC**: Virtual Private Cloud for network isolation
  - Docs: https://docs.aws.amazon.com/vpc/latest/userguide/

- **CloudWatch**: Monitoring and logging
  - Docs: https://docs.aws.amazon.com/cloudwatch/
  - Logs: https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/

- **AWS KMS**: Key management for encryption
  - Docs: https://docs.aws.amazon.com/kms/latest/developerguide/

- **IAM**: Identity and access management
  - Docs: https://docs.aws.amazon.com/iam/

---

## Python Standard Library

### datetime
- **Documentation**: https://docs.python.org/3/library/datetime.html
- **Used For**: Date and time handling
- **Usage**: ISO format timestamps for book records

### math
- **Documentation**: https://docs.python.org/3/library/math.html
- **Used For**: Mathematical calculations
- **Usage**: `ceil()` for pagination calculations

### os
- **Documentation**: https://docs.python.org/3/library/os.html
- **Used For**: Environment variables
- **Usage**: Reading `MONGODB_URI` from environment

### asyncio
- **Documentation**: https://docs.python.org/3/library/asyncio.html
- **Used For**: Asynchronous programming
- **Usage**: Async endpoint handlers in FastAPI

---

## Development Tools

### Git
- **Documentation**: https://git-scm.com/doc
- **Used For**: Version control
- **File**: `.gitignore` for excluding files

### Environment Variables
- **Library**: `python-dotenv`
- **Documentation**: https://github.com/theskumar/python-dotenv
- **Usage**: `.env` file for configuration

---

## Best Practices & Patterns

### SOLID Principles
- **Single Responsibility**: Each module has one purpose
- **Open/Closed**: Code is open for extension, closed for modification
- **Liskov Substitution**: Proper inheritance and polymorphism
- **Interface Segregation**: Specific interfaces rather than general ones
- **Dependency Inversion**: Depend on abstractions, not concretions

### Design Patterns Used
- **Repository Pattern**: Database abstraction layer
- **Dependency Injection**: FastAPI's dependency system
- **Factory Pattern**: Model creation and validation
- **Singleton Pattern**: Global database instance

### Security Best Practices
- **Input Validation**: Pydantic validates all inputs
- **SQL/NoSQL Injection Prevention**: Parameterized queries
- **Error Handling**: Don't expose sensitive information
- **CORS**: Configurable cross-origin requests
- **Encryption**: KMS for database encryption (AWS)

### Performance Best Practices
- **Indexing**: MongoDB indexes on frequently queried fields
- **Pagination**: Limit dataset transfer
- **Connection Pooling**: Reuse database connections
- **Async/Await**: Non-blocking I/O operations
- **Caching**: Can be added to aggregation queries

---

## Code Quality Tools

### Linting & Formatting
- **Recommendations**:
  - `black`: Code formatter
  - `flake8`: Style guide enforcement
  - `pylint`: Code analysis
  - `mypy`: Static type checking

### Type Hints
- **Python 3.10+ Union Types**: `str | None` instead of `Optional[str]`
- **Reference**: https://www.python.org/dev/peps/pep-0604/

---

## API Documentation

### OpenAPI Specification
- **Documentation**: https://spec.openapis.org/
- **Generated By**: FastAPI automatically
- **Access**: `/openapi.json` and `/docs` (Swagger UI)

### Swagger UI
- **Documentation**: https://swagger.io/tools/swagger-ui/
- **Auto-generated**: Available at `/docs`

### ReDoc
- **Documentation**: https://redocly.com/
- **Auto-generated**: Available at `/redoc`

---

## Environment & Configuration

### Environment Variables Used
- `MONGODB_URI`: MongoDB connection string
- `API_HOST`: API host (default: 0.0.0.0)
- `API_PORT`: API port (default: 8000)
- `ENVIRONMENT`: Environment name (development/production)

### Configuration Management
- `.env` file for local development
- Docker environment variables
- Terraform variables for cloud deployment

---

## Monitoring & Logging

### Application Logging
- **Built-in Python logging**: https://docs.python.org/3/library/logging.html
- **CloudWatch Integration**: For cloud deployments

### Health Checks
- **Endpoint**: `/health`
- **Used By**: Load balancers, Kubernetes, monitoring systems

### Metrics Collection
- **CloudWatch Metrics**: CPU, Memory, Request count
- **Custom Metrics**: Can be added to endpoints

---

## Version Information

- **Python**: 3.11+
- **FastAPI**: 0.104.1+
- **PyMongo**: 4.6.1+
- **Pydantic**: 2.5.0+
- **Pytest**: 7.4.3+
- **mongomock**: 4.1.2+

---

## Additional Resources

### FastAPI Best Practices
- https://fastapi.tiangolo.com/deployment/
- https://fastapi.tiangolo.com/advanced/

### MongoDB Best Practices
- https://docs.mongodb.com/drivers/pymongo/current/
- https://docs.mongodb.com/manual/applications/data-models/

### Docker Best Practices
- https://docs.docker.com/develop/dev-best-practices/
- https://docs.docker.com/develop/security-best-practices/

### AWS Best Practices
- https://aws.amazon.com/architecture/best-practices/
- https://docs.aws.amazon.com/general/latest/gr/aws-security-best-practices.html

### RESTful API Design
- https://www.rfc-editor.org/rfc/rfc7231
- https://jsonapi.org/
- https://www.postman.com/api-platform/api-design/

---

## Getting Started with References

1. **Learning FastAPI**: Start with the official tutorial
2. **Understanding MongoDB**: Read the aggregation pipeline docs
3. **API Testing**: Use Swagger UI at `/docs`
4. **Debugging**: Check CloudWatch logs or local terminal output
5. **Deployment**: Follow AWS Terraform documentation

---

**Last Updated**: September 17, 2026
**Maintainer**: Development Team
