import os
import sys
import transaction

from pyramid.config import Configurator
from pyramid_sqlalchemy import Session
from pyramid_sqlalchemy.meta import metadata
from pyramid.paster import get_appsettings, setup_logging

from ..models import ToDo, sample_todos

# run this when changes to the schema have been made

# this is 'fairly standard set of boiler plate for getting arguements from the cmd line'
def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: %s development.ini' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    # callable from main will 'set itself up'
    # Usage and configuration
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    config = Configurator(settings=settings)
    config.include('pyramid_sqlalchemy')

    # uses python context manager
    # Make the database with schema and default data
    with transaction.manager:
        metadata.create_all()
        for todo in sample_todos:
            t = ToDo(title=todo['title'])
            Session.add(t)

