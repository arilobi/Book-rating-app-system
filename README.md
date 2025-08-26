# Book Rating App System

This is a simple book rating system with a Flask backend.

## Getting Started

### Installation
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Database Setup
1. Set the Flask app environment variable:
   ```bash
   export FLASK_APP=run.py
   ```
2. Initialize the database:
   ```bash
   flask db init  # Only needed for the first time
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

### Running the Application
1. Run the application:
   ```bash
   flask run
   ```
The application will be running at `http://127.0.0.1:5000/`.

### Running the Tests
```bash
python tests/test_app.py
```

## API Endpoints

- `POST /books`: Add a new book.
  - Body: `{"title": "Book Title", "author": "Book Author"}`
- `GET /books`: Get all books.
- `GET /books/<book_id>`: Get a specific book.
- `POST /books/<book_id>/rate`: Rate a book.
  - Body: `{"value": 5}`
- `GET /books/<book_id>/rating`: Get the average rating for a book.