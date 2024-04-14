from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(80), nullable=False)
    publisher = db.Column(db.String(120))

    def __repr__(self):
        return f"<Book {self.book_name}, Author: {self.author}, Publisher: {self.publisher}>"

@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    output = [{'id': book.id, 'book_name': book.book_name, 'author': book.author, 'publisher': book.publisher} for book in books]
    return jsonify({"books": output})

@app.route('/books/<id>', methods=['GET'])
def get_book(id):
    book = Book.query.get_or_404(id)
    return jsonify({'id': book.id, 'book_name': book.book_name, 'author': book.author, 'publisher': book.publisher})

@app.route('/books', methods=['POST'])
def add_book():
    book_data = request.get_json()
    book = Book(book_name=book_data['book_name'], author=book_data['author'], publisher=book_data['publisher'])
    db.session.add(book)
    db.session.commit()
    return jsonify({'id': book.id}), 201

@app.route('/books/<id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if book is None:
        return jsonify({"error": "not found"}), 404
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
