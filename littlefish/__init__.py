from flask import Flask

import os

ROOT = os.path.dirname(__file__)

static_folder = os.path.join(ROOT, 'static')
template_folder = os.path.join(ROOT, 'templates')
app = Flask(__name__,
        static_folder=static_folder,
        template_folder=template_folder)
app.config.from_object('littlefish.config.LittlefishConfig')

from littlefish import db
from littlefish import routes
