from pyramid.httpexceptions import HTTPNotFound
from pyramid.security import Allow, Everyone, Deny
from sqlalchemy import (
    Column,
    Integer,
    Text
)
from pyramid_sqlalchemy import BaseObject, Session
from . import ArrayType

class ToDo(BaseObject):
    __tablename__ = 'todo'
    id = Column(Integer, primary_key=True)
    title = Column(Text)
    acl = Column(ArrayType)
    default_acl = [
        (Allow, Everyone, 'view'),
        # they Denial of Jill will not fire because the first acl as already been applied
        (Deny, 'jill', 'view'),
        (Allow, 'group:editors', 'edit')
    ]

    # self=None --
    # we are using this to someone check to see if a preexisting acl is in place
    # honestly not sure why self=None, is this a default argument?
    # how can you call this function without self, what would the point be?
    def __acl__(self=None):
        return getattr(self, 'acl', None) or ToDo.default_acl

def todo_factory(request):
    todo_id = request.matchdict.get('id')
    if todo_id is None:
        # Return the class
        return ToDo
    todo_id_int = int(todo_id)
    todo = Session.query(ToDo).filter_by(id=todo_id_int).first()
    if not todo:
        raise HTTPNotFound()
    return todo

sample_todos = [
    dict(title='Get Milk'),
    dict(title='Get Eggs'),
    dict(title='Secure Task',
         acl=[
             ('Allow', 'group:admins', 'edit'),
             ('Allow', 'group:admins', 'view')
         ]
         )
]
