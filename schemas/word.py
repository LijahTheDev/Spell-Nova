from ma import ma
from models.word import WordModel
from models.list import ListModel


class WordSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WordModel
        load_only = ("list",)
        dump_only = ("id",)
        include_fk = True
