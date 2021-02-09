from flask_restful import Resource, request
from flask_jwt_extended import jwt_required, fresh_jwt_required
from models.word import WordModel
from schemas.word import WordSchema

WORD_ALREADY_EXISTS = "The word '{}' already exists."
ERROR_INSERTING = "An error occurred while inserting the word."
WORD_NOT_FOUND = "Word not found."
WORD_DELETED = "Word deleted."

word_schema = WordSchema()
word_list_schema = WordSchema(many=True)


class Word(Resource):
    @classmethod
    def get(cls):
        word = request.get_json()["word"]

        word = WordModel.find_by_word(word)
        if word:
            return word_schema.dump(word), 200

        return {"message": WORD_NOT_FOUND}, 404

    @classmethod
    @jwt_required
    def post(cls):
        payload = request.get_json()
        word_json = request.get_json()["word"]

        if WordModel.find_by_word(word=word_json):
            return {"message": WORD_ALREADY_EXISTS.format(word=word_json)}, 400

        try:
            word = WordModel(**payload)  # word_schema was throwing error
            word.save_to_db()
        except (Exception, ArithmeticError) as e:
            print(e)
            return {"message": ERROR_INSERTING}, 500

        return word_schema.dump(word), 201

    @classmethod
    @jwt_required
    def delete(cls):
        word = request.get_json()["word"]

        word = WordModel.find_by_word(word)
        if word:
            word.delete_from_db()
            return {"message": WORD_DELETED}, 200

        return {"message": WORD_NOT_FOUND}, 404

    @classmethod
    def put(cls):
        old_word_json = request.get_json()["old_word"]
        new_word_json = request.get_json()["new_word"]

        old_word = WordModel.find_by_word(old_word_json)

        if old_word:
            print('updating old word with new word')
            old_word.word = new_word_json
            old_word.save_to_db()

            return word_schema.dump(old_word), 200
        else:

            print('creating new word from new')
            new_word = word_schema.load(new_word_json)
            new_word.save_to_db()

            return word_schema.dump(new_word), 200


class WordList(Resource):
    @classmethod
    def get(cls):
        return {"words": word_list_schema.dump(WordModel.find_all())}, 200
