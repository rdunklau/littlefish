from flask import render_template, session, request, redirect, url_for
from littlefish import app, db
from littlefish.db import Sequence, TopicDomainClass
# Load routes
from littlefish import sequence, xhr, seance, etape


@app.route('/')
def index():
    sequences = Sequence.query.filter(TopicDomainClass.class_code ==
            session['classe']).all()
    return render_template('index.html', sequences=sequences)


@app.route('/change_class/', methods=('POST',))
def change_class():
    session['classe'] = request.form.get('classe')
    url = session.get('last_url', request.referrer)
    session.pop('last_url', None)
    return redirect(url, code=303)


@app.route('/change_class/', methods=('GET',))
def select_class():
    return render_template('no_class.html')
