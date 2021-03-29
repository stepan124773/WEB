import sqlalchemy
from .db_session import SqlAlchemyBase


class Ad(SqlAlchemyBase):
    __tablename__ = 'Ads'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    city = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
