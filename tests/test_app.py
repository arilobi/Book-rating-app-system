import unittest
import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from run import app
from app.models import db

class BookRatingTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_book(self):
        response = self.app.post('/books',
                                 data=json.dumps({'title': 'Test Book', 'author': 'Test Author'}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_get_all_books(self):
        self.app.post('/books',
                      data=json.dumps({'title': 'Test Book', 'author': 'Test Author'}),
                      content_type='application/json')
        response = self.app.get('/books')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(len(data['books']), 1)

    def test_get_one_book(self):
        post_response = self.app.post('/books',
                                      data=json.dumps({'title': 'Test Book', 'author': 'Test Author'}),
                                      content_type='application/json')
        response = self.app.get('/books/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data['title'], 'Test Book')

    def test_rate_book(self):
        self.app.post('/books',
                      data=json.dumps({'title': 'Test Book', 'author': 'Test Author'}),
                      content_type='application/json')
        response = self.app.post('/books/1/rate',
                                 data=json.dumps({'value': 5}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_get_book_rating(self):
        self.app.post('/books',
                      data=json.dumps({'title': 'Test Book', 'author': 'Test Author'}),
                      content_type='application/json')
        self.app.post('/books/1/rate',
                      data=json.dumps({'value': 5}),
                      content_type='application/json')
        response = self.app.get('/books/1/rating')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data['average_rating'], 5)

if __name__ == '__main__':
    unittest.main()
