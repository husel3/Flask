from marshmallow import Schema, fields

# This is the structure for book data 
class BookSchema(Schema):
    id = fields.Str(dump_only=True)  # ID is created automatically, we don't send it when adding a book
    title = fields.Str(required=True)  # Title is required
    price = fields.Float(required=True)  # Price is required and must be a number
    library_id = fields.Str(required=True)  # Each book must belong to a library (using its ID)

# This is for updating a book (we usually only update title and price)
class BookUpdateSchema(Schema):
    title = fields.Str(required=True)  # New title
    price = fields.Float(required=True)  # New price

# This is the structure for library data
class LibrarySchema(Schema):
    id = fields.Str(dump_only=True)  # Library ID is created automatically
    name = fields.Str(required=True)  # Library name is required
