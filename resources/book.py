import uuid  # to generate unique IDs for new books

from flask.views import MethodView  # for creating class-based views
from flask import request  # to access request data (not used here but often useful)
from flask_smorest import Blueprint, abort  # Blueprint for routing, abort for error handling

from db import books, libraries 
from schemas import BookSchema, BookUpdateSchema  # import schemas to validate and format data

# Create a Blueprint for book-related routes
blp = Blueprint('books', __name__, description='Operations on books')

# This route handles operations for a single book (GET, PUT, DELETE)
@blp.route("/book/<string:book_id>")
class Book(MethodView):

    # GET a book by its ID
    @blp.response(200, BookSchema)
    def get(self, book_id):
        try:
            return books[book_id]  # return the book if it exists
        except KeyError:
            abort(404, message="Book not found.")  # return error if not found

    # DELETE a book by its ID
    def delete(self, book_id):
        try:
            del books[book_id]  # delete the book
            return {"message": "Book deleted."}
        except KeyError:
            abort(404, message="Book not found.")

    # UPDATE a book's info using PUT
    @blp.arguments(BookUpdateSchema)  # validate input data using schema
    @blp.response(200, BookSchema)
    def put(self, book_data, book_id):
        try:
            book = books[book_id]  # get the existing book
            book.update(book_data)  # update its data
            return book
        except KeyError:
            abort(404, message="Book not found.")

# This route handles operations for the list of books (GET all, POST new)
@blp.route("/book")
class BookList(MethodView):

    # GET all books
    @blp.response(200, BookSchema(many=True))  # "many=True" means it's a list of books
    def get(self):
        return list(books.values())  # return all books as a list

    # POST (add) a new book
    @blp.arguments(BookSchema)  # validate input using full BookSchema
    @blp.response(201, BookSchema)
    def post(self, book_data):
        # Check if the library exists
        if book_data["library_id"] not in libraries:
            abort(404, message="Library not found.")

        # Check for duplicate book title in the same library
        for book in books.values():
            if (
                book_data["title"] == book["title"]
                and book_data["library_id"] == book["library_id"]
            ):
                abort(400, message=f"Book '{book_data['title']}' already exists.")

        # Create a new book with a unique ID
        book_id = uuid.uuid4().hex
        new_book = {**book_data, "id": book_id}
        books[book_id] = new_book  # save the book in the "database"

        return new_book  # return the new book
