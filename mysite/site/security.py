from sqlalchemy.orm.exc import NoResultFound
from pyramid_sqlalchemy import Session

from ..users.models import User


def groupfinder(username, request):
    groups = []
    try:
        user = Session.query(User).filter(User.username == username).one()
    except NoResultFound:
        pass
    else:
        groups = user.groups
    return groups
