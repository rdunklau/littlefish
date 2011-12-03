#!/usr/bin/env python2
from littlefish import app
from flup.server.fcgi import WSGIServer

WSGIServer(app).run()
