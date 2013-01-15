"""Base views"""
from flask import (render_template, session, request, redirect, url_for,
    send_from_directory, flash)
from littlefish import app, db
from littlefish.db import Sequence, TopicDomainClass, Topic, Domain, User
# Load routes
from littlefish import sequence, xhr, seance, etape
from flaskext.wtf import Form, validators
from littlefish.dojo import TextField, PasswordField
from passlib.apps import custom_app_context as pwd_ctx

@app.route('/')
def index():
    """Index page"""
    return sequences_page(session['user'])


def sequences_page(user=None):
    sequences = (Sequence.query
                .select_from(Sequence)
                .join(TopicDomainClass)
                .join(Domain)
                .join(Topic)
                .order_by(Domain.label, Topic.label))
    if session.get('classe', None):
    	sequences = sequences.filter(
		TopicDomainClass.class_code == session['classe'])

    if user:
      sequences = sequences.filter(Sequence.user_login==user)
    sequences = sequences.all()
    return render_template('index.html', sequences=sequences,
		    user=user)


@app.route('/sequences/<string:user>/')
@app.route('/sequences/')
def user_sequences(user=None):
    """Index page"""
    return sequences_page(user)


@app.route('/change_class/', methods=('GET', 'POST',))
def change_class():
    """Class selection post url"""
    session['classe'] = request.values.get('classe', None)
    if not session['classe']:
  	return render_template('no_class.html')
    url = session.get('last_url', request.referrer)
    session.pop('last_url', None)
    return redirect(url, code=303)



class LoginForm(Form):
  login = TextField()
  password = PasswordField()

@app.route('/login/', methods=('GET', 'POST'))
def login():
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(login=form.login.data).first()
    if user and pwd_ctx.verify(form.password.data, user.password):
      session['user'] = user.login
      return redirect('/', code=303)
    else:
      flash(u'Mauvais login ou mot de passe')
  return render_template('wtforms/form.jinja2', form=form,
            title=u'Se connecter')

@app.route('/disconnect/')
def disconnect():
  session.pop('user', None)
  return redirect('/', code=303)
