import uuid #to generate unique IDs

#to create the web app and request to handle incoming HTTP request data.
from flask import Flask, request
from flask_smorest import Api

# importing blueprints for books and libraries
from resources.book import blp as BookBlueprint
from resources.library import blp as LibraryBlueprint

app = Flask(__name__) #to create the Flask app instance

#to check directly from web
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Libraries REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.1.0"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app) #to create an API object

# register blueprints 
api.register_blueprint(BookBlueprint)
api.register_blueprint(LibraryBlueprint)
