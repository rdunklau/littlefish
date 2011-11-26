from flask import render_template, session, request, redirect, url_for
from littlefish import app, db

# Load routes
from littlefish import sequence, xhr

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/change_class/', methods=('POST',))
def change_class():
    session['classe'] = request.form.get('classe')
    url = session.get('last_url', request.referrer)
    session.pop('last_url', None)
    return redirect(url, code=303)


@app.route('/change_class/', methods=('GET',))
def select_class():
    return render_template('no_class.html')
