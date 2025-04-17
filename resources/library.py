import uuid  # to create unique IDs for libraries

from flask import request
from flask.views import MethodView  # allows us to organize routes as classes
from flask_smorest import Blueprint, abort  # Blueprint groups routes; abort handles errors

from db import libraries  # our in-memory "database"
from schemas import LibrarySchema  # schema for validating library data

# Create a blueprint for library-related routes
blp = Blueprint("libraries", __name__, description="Operations on libraries")

# This route handles a single library (GET and DELETE by ID)
@blp.route("/library/<string:library_id>")
class Library(MethodView):
    
    # Get one library by ID
    @blp.response(200, LibrarySchema)
    def get(self, library_id):
        try:
            return libraries[library_id]  # return the library data
        except KeyError:
            abort(404, message="Library not found.")  # error if not found

    # Delete a library by ID
    def delete(self, library_id):
        try:
            del libraries[library_id]  # remove from our "database"
            return {"message": "Library deleted."}
        except KeyError:
            abort(404, message="Library not found.")  # error if it doesn't exist

# This route handles all libraries (GET all and POST new)
@blp.route("/library")
class LibraryList(MethodView):
    
    # Get all libraries
    def get(self):
        return {"libraries": list(libraries.values())}  # return all as a list

    # Add a new library
    @blp.arguments(LibrarySchema)  # validate input
    @blp.response(200, LibrarySchema)
    def post(self, library_data):
        # Make sure "name" is included in the request
        if "name" not in library_data:
            abort(400, message="Bad request. Ensure 'name' is included.")

        # Check if the library already exists (by name)
        for library in libraries.values():
            if library_data["name"] == library["name"]:
                abort(400, message=f"Library '{library_data['name']}' already exists.")

        # Create a new library with a unique ID
        library_id = uuid.uuid4().hex
        new_library = {**library_data, "id": library_id}
        libraries[library_id] = new_library  # store it

        return new_library, 201  # return the new library with 201 Created
