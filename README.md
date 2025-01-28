# Library Management System API

A Django RESTful API for managing a library's book collection. This system provides comprehensive endpoints for book management with features like pagination, rate limiting, and filtering.

## Features

- CRUD operations for books
- Pagination support (5 items per page)
- Rate limiting (100 requests per minute)
- Advanced filtering options
- Input validation
- Comprehensive error handling
- Custom response formatting

## Tech Stack

- Django
- Django REST Framework
- Django Filter Backend
- Python 3.x

## Models

### Book
The system manages books with the following attributes:

- Title (required, min 2 characters)
- Author (required, min 2 characters)
- Genre (choices available)
- Publication Date (must not be in future)
- Availability Status
- Edition (must be a positive integer)
- Summary (min 10 characters)

Available genres include Fiction, Non-Fiction, Science Fiction, Fantasy, Mystery, and many more.

Availability status can be:
- Available
- Checked Out
- Lost
- Damaged

## API Endpoints

### Books API

```
GET /api/v1/books/         - List all books (paginated)
POST /api/v1/books/        - Create a new book
GET /api/v1/books/{id}/    - Retrieve a specific book
PUT /api/v1/books/{id}/    - Update a specific book
DELETE /api/v1/books/{id}/ - Delete a specific book
```
```
POSTMAN TEST
GET  https://library1212.pythonanywhere.com/api/v1/books/                  - List all books (paginated)
POST https://library1212.pythonanywhere.com/api/v1/books/                  - Create a new book
GET  https://library1212.pythonanywhere.com/api/v1/books/1/               - Retrieve a specific book
PUT  https://library1212.pythonanywhere.com/api/v1/books/1/               - Update a specific book
DELETE  https://library1212.pythonanywhere.com/api/v1/books/1/            - Delete a specific book
```


### Query Parameters

- `page`: Page number for pagination
- `page_size`: Number of items per page (max 100)
- `genre`: Filter by genre
- `author`: Filter by author
- `availability`: Filter by availability status

## Rate Limiting

The API implements rate limiting with the following constraints:
- 100 requests per minute for anonymous users
- Rate limit headers included in responses:
  - `X-RateLimit-Limit`
  - `X-RateLimit-Remaining`
  - `X-RateLimit-Reset`

## Response Format

### Success Response

```json
{
    "status": "success",
    "message": "Operation successful",
    "book": {
        "id": 1,
        "title": "Sample Book",
        "author": "John Doe",
        "genre": "Fiction",
        "publication_date": "2024-01-01",
        "availability": "Available",
        "edition": "1",
        "summary": "A sample book summary"
    },
    
    "status": "success",
    "message": "Book details retrieved successfully",
    "headers": {
        "X-RateLimit-Limit": 100,
        "X-RateLimit-Remaining": 99,
        "X-RateLimit-Reset": 1668144600
    }
}

```

### Error Response

```json
{
    "status": "failed",
    "message": "Invalid data provided",
    "errors": {
        "field_name": [
            "Error message"
        ]
    },
    "headers": {
        "X-RateLimit-Limit": 100,
        "X-RateLimit-Remaining": 99,
        "X-RateLimit-Reset": 1737986843
    }
}
```

## Validation Rules

- Title: Minimum 2 characters
- Author: Minimum 2 characters
- Publication Date: Cannot be in the future
- Edition: Must be a positive integer
- Summary: Minimum 10 characters

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
```

2. Create and activate a virtual environment:
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Start the development server:
```bash
python manage.py runserver
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request


