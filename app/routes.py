from flask import request, jsonify, Blueprint
from .models import db, Book, Rating, User
from flask_login import login_user, logout_user, login_required, current_user
from functools import wraps

bp = Blueprint('api', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            return jsonify({'message': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'client')  # Default role is 'client'

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 400

    new_user = User(username=username, role=role)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return jsonify({'message': 'Invalid credentials'}), 401

    login_user(user)
    return jsonify({'message': 'Logged in successfully'})

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'})

@bp.route('/books', methods=['POST'])
@login_required
@admin_required
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
