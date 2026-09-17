# Quick Start Guide

Get the Books API running in minutes.

## 🚀 Fastest Way (Docker Compose)

```bash
docker-compose up -d
```

That's it! API is running at `http://localhost:8000`

- **Swagger UI**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

Stop with: `docker-compose down`

---

## 🐍 Local Development

### 1. Install Dependencies
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Start MongoDB
```bash
docker run -d -p 27017:27017 mongo:7.0
```

### 3. Run API
```bash
uvicorn main:app --reload
```

---

## 📝 Quick Test

```bash
# Get all books
curl http://localhost:8000/books

# Create a book
curl -X POST http://localhost:8000/books \
  -H "Content-Type: application/json" \
  -d '{
    "id": 10,
    "title": "My Book",
    "author": "My Author",
    "publisher": "My Publisher",
    "pages": 300
  }'

# Get specific book
curl http://localhost:8000/books/10

# Update book
curl -X PATCH http://localhost:8000/books/10 \
  -H "Content-Type: application/json" \
  -d '{"pages": 350}'

# Delete book
curl -X DELETE http://localhost:8000/books/10
```

---

## 🧪 Run Tests

```bash
pytest -v
```

---

## 📚 Full Documentation

See `README.md` for complete documentation.

## 🏗️ Deploy to AWS

See `terraform/TERRAFORM_README.md` for AWS deployment.
