from ma import ma
from models.user import UserModel


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_only = ("password",)  # Will be ignored when dumping
        dump_only = ("id",)  # Will be ignored when loading
        load_instance = True
