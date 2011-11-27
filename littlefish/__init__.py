from flask import Flask, g, session, redirect, url_for, request
import psycopg2
import psycopg2.extensions
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

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


@app.before_request
def inject_classes():
    if ('classe' not in session and
            request.endpoint not in ('static', 'change_class', 'select_class')
            and request.url != '/favicon.ico'):
        session['last_url'] = request.url
        return redirect(url_for('select_class'), 303)
    g.classes = db.Class.query.all()
