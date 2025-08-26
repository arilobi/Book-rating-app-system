from flask import request, jsonify, Blueprint
from .models import db, Book, Rating

bp = Blueprint('api', __name__)

@bp.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    new_book = Book(title=data['title'], author=data['author'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'New book added!'})

@bp.route('/books', methods=['GET'])
def get_all_books():
    books = Book.query.all()
    output = []
    for book in books:
        book_data = {}
        book_data['id'] = book.id
        book_data['title'] = book.title
        book_data['author'] = book.author
        output.append(book_data)
    return jsonify({'books': output})

@bp.route('/books/<book_id>', methods=['GET'])
def get_one_book(book_id):
    book = Book.query.get_or_404(book_id)
    book_data = {}
    book_data['id'] = book.id
    book_data['title'] = book.title
    book_data['author'] = book.author
    return jsonify(book_data)

@bp.route('/books/<book_id>/rate', methods=['POST'])
def rate_book(book_id):
    book = Book.query.get_or_404(book_id)
    data = request.get_json()
    new_rating = Rating(value=data['value'], book_id=book.id)
    db.session.add(new_rating)
    db.session.commit()
    return jsonify({'message': 'Book rated!'})

@bp.route('/books/<book_id>/rating', methods=['GET'])
def get_book_rating(book_id):
    book = Book.query.get_or_404(book_id)
    ratings = book.ratings
    if not ratings:
        return jsonify({'message': 'No ratings for this book yet.'})

    total = sum(rating.value for rating in ratings)
    average = total / len(ratings)
    return jsonify({'average_rating': average})
