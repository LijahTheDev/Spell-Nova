from ma import ma
from models.list import ListModel
from models.word import WordModel
from schemas.word import WordSchema


class ListSchema(ma.SQLAlchemyAutoSchema):
    words = ma.Nested(WordSchema, many=True)

    class Meta:
        model = ListModel
        dump_only = ("id",)  # Will be ignored when loading
        include_fk = True
