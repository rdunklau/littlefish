#!/usr/bin/env python2
from littlefish import app
from flup.server.fcgi import WSGIServer

app.config['SECRET_KEY'] = 'sklajdlkaj'

WSGIServer(app).run()
