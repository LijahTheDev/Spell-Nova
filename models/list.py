from typing import List
from db import db


class ListModel(db.Model):
    __tablename__ = "lists"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)

    words = db.relationship('WordModel', lazy='dynamic')

    @classmethod
    def find_by_name(cls, name: str) -> "ListModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls) -> List["ListModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
