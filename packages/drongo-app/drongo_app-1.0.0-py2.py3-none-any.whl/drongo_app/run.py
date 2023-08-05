#!/usr/bin/env python3

import logging
import os
import shutil
import sys


NEST = shutil.which('drongo-nest')


def run_dev():
    LOGGING_FORMAT = (
        '\033[36m%(asctime)-24s \033[34m%(name)-16s '
        '\033[32m%(levelname)-8s \033[97m%(message)s\033[39m'
    )
    logging.basicConfig(format=LOGGING_FORMAT, level=logging.INFO)

    os.environ['DRONGO_SETTINGS_FILE'] = os.path.realpath(sys.argv[1])
    from nest import Nest
    from drongo_app.app import app

    server = Nest(app=app, auto_reload=True)
    try:
        server.run()
    except KeyboardInterrupt:
        print('Terminating...')
        server.shutdown()


def run():
    from nest import Nest
    from drongo_app.app import app

    os.environ['DRONGO_SETTINGS_FILE'] = os.path.realpath(sys.argv[1])

    server = Nest(app=app)
    try:
        server.run()
    except KeyboardInterrupt:
        print('Terminating...')
        server.shutdown()


if __name__ == '__main__':
    run()
