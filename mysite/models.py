from pyramid.httpexceptions import HTTPNotFound
from sqlalchemy import (
    Column,
    Integer,
    Text
)
from pyramid_sqlalchemy import BaseObject, Session


class ToDo(BaseObject):
    __tablename__ = 'todo'
    id = Column(Integer, primary_key=True)
    title = Column(Text, unique=True)

    def __json__(self, request):
        return dict(id=self.id, title=self.title)

    @classmethod
    def by_id(cls, todo_id):
        return Session.query(cls).filter_by(id=int(todo_id)).first()

    @classmethod
    def list(cls):
        return Session.query(cls).order_by(cls.title).all()

def todo_factory(request):
    todo = ToDo.by_id(request.matchdict.get('id'))
    if not todo:
        raise HTTPNotFound()
    return todo


sample_todos = [
    dict(title='Get Milk'),
    dict(title='Get Eggs')
]
