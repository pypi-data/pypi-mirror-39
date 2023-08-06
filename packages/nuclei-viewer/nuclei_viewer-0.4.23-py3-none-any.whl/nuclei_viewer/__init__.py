from flask import Flask
import dash
from flask_caching import Cache
from .version import __version__

app = Flask(__name__)
page = dash.Dash(server=app)
page.config.suppress_callback_exceptions = True
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

import nuclei_viewer.main