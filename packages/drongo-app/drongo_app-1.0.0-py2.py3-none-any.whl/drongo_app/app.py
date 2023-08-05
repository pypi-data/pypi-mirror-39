import importlib
import logging
import os
import sys
import yaml

from drongo import Drongo

from .mw import CORSMiddleware
from .options import evaluate


fmt = (
    '\033[36m%(asctime)-24s \033[34m%(name)-16s '
    '\033[32m%(levelname)-8s \033[97m%(message)s\033[39m'
)
logging.basicConfig(format=fmt, level=logging.WARNING)

app = Drongo()


def dummy(ctx):
    return ''


app.add_url(pattern='/*', method='OPTIONS', call=dummy)

app.add_middleware(CORSMiddleware())

env = {}
BASE_DIR = env['BASE_DIR'] = os.environ.get('BASE_DIR', os.path.realpath('.'))

for k, v in os.environ.items():
    env['env__' + k] = v

settings_file = os.environ.get('DRONGO_SETTINGS_FILE', None)
settings = {}

if settings_file is not None:
    with open(settings_file) as fd:
        settings = yaml.load(fd)

# Prepare python paths
for module in settings.get('modules'):
    # FIXME: This will not work later on. Find an alternative.
    sys.path.append(os.path.join(BASE_DIR, '_core', module['name']))
    sys.path.append(os.path.join(BASE_DIR, '_modules', module['name']))

for module in settings.get('modules', []):
    m = '.'.join(module['class'].split('.')[:-1])
    c = module['class'].split('.')[-1]
    cls = getattr(importlib.import_module(m), c)
    options = module.get('app', {}).get('options', {})
    options = evaluate(options, env)
    cls(
        app,
        **options
    )
