from flask_restful import Resource, request
from models.list import ListModel
from schemas.list import ListSchema

NAME_ALREADY_EXISTS = "A list with name '{}' already exists."
ERROR_INSERTING = "An error occurred while inserting the list."
LIST_NOT_FOUND = "List not found."
LIST_DELETED = "List deleted."

list_schema = ListSchema()
list_list_schema = ListSchema(many=True)


class List(Resource):
    @classmethod
    def get(cls):
        name = request.get_json()["name"]

        list = ListModel.find_by_name(name)
        if list:
            return list_schema.dump(list), 200

        return {"message": LIST_NOT_FOUND}, 404

    @classmethod
    def post(cls):
        name = request.get_json()["name"]

        if ListModel.find_by_name(name):
            return {"message": NAME_ALREADY_EXISTS.format(name=name)}, 400

        list = ListModel(name=name)
        try:
            list.save_to_db()
        except:
            return {"message": ERROR_INSERTING}, 500

        return list_schema.dump(list), 201

    @classmethod
    def delete(cls):
        name = request.get_json()["name"]

        list = ListModel.find_by_name(name)
        if list:
            list.delete_from_db()
            return {"message": LIST_DELETED}, 200

        return {"message": LIST_NOT_FOUND}, 404


class ListList(Resource):
    @classmethod
    def get(cls):
        return {"lists": list_list_schema.dump(ListModel.find_all())}, 200
