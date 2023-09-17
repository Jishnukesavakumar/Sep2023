from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample book data
books = [
    {
        "id": 1,
        "title": "Python Crash Course",
        "author": "Eric Matthes",
        "published_year": 2015,
    },
    {
        "id": 2,
        "title": "Flask Web Development",
        "author": "Miguel Grinberg",
        "published_year": 2018,
    },
]

# Create a new book
@app.route("/books", methods=["POST"])
def create_book():
    data = request.get_json()
    if "title" in data and "author" in data and "published_year" in data:
        new_book = {
            "id": len(books) + 1,
            "title": data["title"],
            "author": data["author"],
            "published_year": data["published_year"],
        }
        books.append(new_book)
        return jsonify({"message": "Book created successfully"}), 201
    else:
        return jsonify({"error": "Incomplete data"}), 400

# Retrieve all books
@app.route("/books", methods=["GET"])
def get_books():
    return jsonify(books)

# Retrieve a specific book by ID
@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = next((book for book in books if book["id"] == book_id), None)
    if book:
        return jsonify(book)
    else:
        return jsonify({"error": "Book not found"}), 404

# Update a book by ID
@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    data = request.get_json()
    book = next((book for book in books if book["id"] == book_id), None)
    if book:
        book["title"] = data.get("title", book["title"])
        book["author"] = data.get("author", book["author"])
        book["published_year"] = data.get("published_year", book["published_year"])
        return jsonify({"message": "Book updated successfully"}), 200
    else:
        return jsonify({"error": "Book not found"}), 404

# Delete a book by ID
@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    global books
    original_length = len(books)
    books = [book for book in books if book["id"] != book_id]
    if len(books) < original_length:
        return jsonify({"message": "Book deleted successfully"}), 200
    else:
        return jsonify({"error": "Book not found"}), 404

if __name__ == "__main__":
    app.run(port = 5001)
