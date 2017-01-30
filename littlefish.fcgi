#!/usr/bin/env python
from flipflop import WSGIServer
from littlefish import app
from werkzeug.contrib.fixers import CGIRootFix

app.config['SECRET_KEY'] = 'sklajdlkaj'

app = CGIRootFix(app)

WSGIServer(app).run()
