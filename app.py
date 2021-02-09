import os
from dotenv import load_dotenv

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError

from ma import ma
from db import db
from blacklist import BLACKLIST
from resources.user import UserRegister, UserLogin, User, TokenRefresh, UserLogout
from resources.word import Word, WordList
from resources.list import List, ListList

load_dotenv()

MWD_API_KEY = os.getenv('MWD_API_KEY')  # Merriam-Webster Dictionary API Key
APP_SECRET = os.getenv('APP_SECRET')
DB_URI = os.getenv('DB_URI')
PORT = os.getenv('PORT') or 5000

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = [
    "access",
    "refresh",
]
app.secret_key = APP_SECRET

api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()

# Handler Validation Errors in Resources
@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


jwt = JWTManager(app)


# This method will check if a token is blacklisted, and will be called automatically when blacklist is enabled
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST


api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")

api.add_resource(Word, "/word")
api.add_resource(WordList, "/words")

api.add_resource(List, "/list")
api.add_resource(ListList, "/lists")

if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    app.run(port=PORT, debug=True)
