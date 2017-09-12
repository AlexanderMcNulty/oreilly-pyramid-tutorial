from sqlalchemy.orm.exc import NoResultFound
from pyramid_sqlalchemy import Session

from .models.users import User

# old version
    # list of fake users which we should use
    #USERS = {'editor': 'editor',
    #         'viewer': 'viewer'}
    #GROUPS = {'editor': ['group:editors']}

    # this is a callback function, decode incoming information from the cookie
    # we then look up that information our system, if we find a user return a list of principles.
    # password validation is not done here, password validation must have been done first.
    #def groupfinder(userid, request):
    #    if userid in USERS:
    #        return GROUPS.get(userid, [])

def groupfinder(username, request):
    groups = []
    try:
        # query for users
        user = Session.query(User).filter(User.username == username).one()
    except NoResultFound:
        pass
    else:
        # return found users groups
        groups = user.groups
    return groups
