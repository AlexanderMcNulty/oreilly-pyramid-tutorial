from sqlalchemy import (
    Column,
    String,
    Integer
)
from pyramid_sqlalchemy import BaseObject

# SQLite doesn't support arrays, workaround
from . import ArrayType


class User(BaseObject):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(120), unique=True)
    password = Column(String(120))
    first_name = Column(String(120))
    last_name = Column(String(120))
    groups = Column(ArrayType)


sample_users = [
    dict(
        id=1,
        username='jill',
        password='jill1',
        first_name='Jill',
        last_name='Smith',
        groups=['group:editors']
    ),
    dict(
        id=2,
        username='jack',
        password='jack2',
        first_name='Jack',
        last_name='Jones',
        groups=[]
    )
]
