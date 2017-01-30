# -*- coding: utf-8 -*-
"""Base views"""
from flask import (render_template, session, request, redirect, url_for,
    send_from_directory, flash)
from littlefish import app, db
from littlefish.db import Sequence, TopicDomainClass, Topic, Domain, User, db
# Load routes
from littlefish import sequence, xhr, seance, etape
from wtforms import validators
from littlefish.forms import Form
from littlefish.dojo import TextField, PasswordField
from passlib.apps import custom_app_context as pwd_ctx

@app.route('/')
def index():
    """Index page"""
    return render_template("index.html")


def sequences_page(user=None, domain=None):
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
    domains = Domain.query.all()
    if domain:
      sequences = sequences.filter(Domain.code==domain)
    sequences = sequences.all()
    return render_template('sequences.html', sequences=sequences,
		    domain_code=domain,
		    user=user, domains=domains)


@app.route('/sequences/<string:user>/')
@app.route('/sequences/')
def user_sequences(user=None):
    """Index page"""
    return sequences_page(user)

@app.route('/domain/<string:domain>/')
@app.route('/domain/<string:domain>/<string:user>/')
def domain(domain, user=None):
    """Index page"""
    return sequences_page(user=user, domain=domain)




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
      flash(u'Mauvais login ou mot de passe', 'error')
  return render_template('wtforms/form.jinja2', form=form,
            title=u'Se connecter')

@app.route('/disconnect/')
def disconnect():
  session.pop('user', None)
  return redirect('/', code=303)

class RegisterForm(Form):
  login = TextField('Login', [validators.Required()])
  password = PasswordField('Mot de passe', [validators.Required()])
  password_bis = PasswordField(u'Mot de passe (vérification)',
                  [validators.equal_to('password')])
  firstname = TextField(u'Prénom', [validators.Required()])
  lastname = TextField('Nom', [validators.Required()])
  email = TextField('Courriel', [validators.Required()])

@app.route('/register/', methods=('GET', 'POST'))
def register():
  form = RegisterForm()
  if form.validate_on_submit():
    if User.query.filter_by(login=form.login.data).first():
        flash(u'Ce login est déjà pris', 'error')
        return render_template('wtforms/form.jinja2', form=form,
            title=u"S'inscrire")
    user = User()
    form.populate_obj(user)
    user.password = pwd_ctx.encrypt(user.password)
    db.session.add(user)
    session['user'] = user.login
    db.session.commit()
    flash(u'Félicitations, votre compte a été créé', 'success')
    return redirect(url_for('user_sequences'))
  return render_template('wtforms/form.jinja2', form=form,
            title=u"S'inscrire")
