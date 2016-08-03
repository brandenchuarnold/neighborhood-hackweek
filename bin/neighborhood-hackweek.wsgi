#!/Users/brandenarnold/env/clean2.7/bin/python

import os

join = os.path.join
base = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
base = os.path.dirname(base)

import sys
sys.path[0:0] = [
    base,
    join(base, 'eggs/zillowdb-0.4.0.b_r8-py2.7.egg'),
    join(base, 'eggs/z_logging_formatters-1.0.136.master.330d7b3-py2.7.egg'),
    join(base, 'eggs/setuptools-5.2-py2.7.egg'),
    join(base, 'eggs/flask_transmute-0.2.14-py2.7.egg'),
    join(base, 'eggs/PyYAML-3.10-py2.7-macosx-10.11-intel.egg'),
    join(base, 'eggs/Flask-0.10.1-py2.7.egg'),
    join(base, 'eggs/pymssql-2.1.1-py2.7-macosx-10.11-intel.egg'),
    join(base, 'eggs/SQLAlchemy-0.6.7-py2.7.egg'),
    join(base, 'eggs/tornado-3.1-py2.7.egg'),
    join(base, 'eggs/flask_restplus-0.8.5-py2.7.egg'),
    join(base, 'eggs/itsdangerous-0.24-py2.7.egg'),
    join(base, 'eggs/Jinja2-2.7.1-py2.7.egg'),
    join(base, 'eggs/Werkzeug-0.10.1-py2.7.egg'),
    join(base, 'eggs/aniso8601-0.92-py2.7.egg'),
    join(base, 'eggs/pytz-2014.10-py2.7.egg'),
    join(base, 'eggs/jsonschema-2.4.0-py2.7.egg'),
    join(base, 'eggs/Flask_RESTful-0.3.2-py2.7.egg'),
    join(base, 'eggs/MarkupSafe-0.15-py2.7-macosx-10.11-intel.egg'),
    join(base, 'eggs/six-1.9.0-py2.7.egg'),
    ]



from neighborhood_hackweek.main import app as application

import neighborhood_hackweek.main

if __name__ == '__main__':
    sys.exit(neighborhood_hackweek.main.main())
