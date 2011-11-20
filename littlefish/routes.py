from flask import render_template
from littlefish import app, db

# Load routes
from littlefish import sequence, xhr

@app.route('/')
def index():
    return render_template('index.html')


