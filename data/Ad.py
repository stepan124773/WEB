
from sqlalchemy import orm
import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin


from sqlalchemy_serializer import SerializerMixin


class Ad(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'Ads'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    address = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    number = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    category = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    photo =sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')
