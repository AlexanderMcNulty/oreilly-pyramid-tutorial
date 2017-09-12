from pyramid.security import Allow, Everyone

class Root(object):
    # access control list
    __acl__ = [(Allow, Everyone, 'view'),
               (Allow, 'group:editors', 'edit')]

    def __init__(self, request):
        pass
