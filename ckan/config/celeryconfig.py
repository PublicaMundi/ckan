import os
import pkg_resources
import ConfigParser as configparser

here = os.path.dirname(os.path.realpath(__file__))
src_dir = os.path.realpath(os.path.join(here, '..', '..'))
config_file = os.path.join(src_dir, 'config.ini')

if not os.path.isfile(config_file):
    raise ValueError('Cannot find configuration under %s' % (config_file))

config = configparser.ConfigParser(defaults={'here': src_dir})
config.read(config_file)

# Set basic configuration options

if config.has_section('app:celery'):
    _g = globals()
    for k, v in config.items('app:celery'):
        if k in ['here', 'debug']:
            continue
        elif k in ['celery_accept_content']:
            _g[k.upper()] = v.split() 
        else:
            _g[k.upper()] = v
else: 
    sqla_url = config.get('app:main', 'sqlalchemy.url')
    BROKER_BACKEND = 'sqlalchemy'
    BROKER_URL = sqla_url
    CELERY_RESULT_BACKEND = "database"
    CELERY_RESULT_DBURI = sqla_url
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_ACCEPT_CONTENT = ['json']

# Collect all registered tasks from entry points

CELERY_IMPORTS = []
for e in pkg_resources.iter_entry_points('ckan.celery_task'):
    f = e.load()
    CELERY_IMPORTS.extend(f())

# Instruct ckan.lib.celery_app where to find configuration

os.environ['CKAN_CONFIG'] = config_file
