from typing import List
from db import db


class WordModel(db.Model):
    __tablename__ = 'words'

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(80), nullable=False, unique=True)

    list_id = db.Column(db.Integer, db.ForeignKey('lists.id'), nullable=False)
    list = db.relationship('ListModel')

    @classmethod
    def find_by_word(self, word: str) -> "WordModel":
        return self.query.filter_by(word=word).first()

    @classmethod
    def find_all(self) -> List["WordModel"]:
        return self.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
