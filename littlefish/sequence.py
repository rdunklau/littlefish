# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for
from littlefish import app
from littlefish.db import db, Class, Sequence, DomainClass, TopicDomainClass,\
    Domain, Topic
from littlefish.dojo import TextField, SelectField, TreeField, TreeLevel
from littlefish.utils import storify

from flaskext.wtf import Form, validators

@app.route('/sequence/xhr/Class/')
def classes_select():
    return storify(db.session.query(Class.code.label('id'), Class.label).all())

@app.route('/sequence/xhr/Domain')
def domain_select():
    return storify(db.session.query(DomainClass.id,
            Domain.label,
            Class.code.label('parent'))
        .select_from(DomainClass)
        .join(Domain)
        .join(Class)
        .all())

@app.route('/sequence/xhr/Topic')
def topic_select():
    return storify(db.session.query(TopicDomainClass.id,
            Topic.label,
            DomainClass.id.label('parent'))
        .select_from(TopicDomainClass)
        .join(DomainClass)
        .join(Topic)
        .all())



class SequenceForm(Form):
    title = TextField(u'Titre', [validators.Required()])
    grade = TreeField(u'Niveau/Discipline', levels=[
        TreeLevel('Classe', '/sequence/xhr/Class'),
        TreeLevel('Domaine Disciplinaire', '/sequence/xhr/Domain'),
        TreeLevel('Discipline', '/sequence/xhr/Topic')])

@app.route('/sequence/<int:sequence_id>')
def sequence(sequence_id):
    seq = Sequence.query.get_or_404(sequence_id)
    return render_template('sequence.html')


@app.route('/sequence/add/', methods=('GET', 'POST'))
def add_sequence():
    classes = Class.query.all()
    form = SequenceForm()
    form.grade.choices = [(grade.code, grade.label) for grade in classes]
    if form.validate_on_submit():
        seq = Sequence()
        form.populate_obj(seq)
        db.session.add(seq)
        db.session.commit()
        return redirect(url_for('sequence', sequence_id=seq.id), code=303)
    return render_template('wtforms/form.jinja2', form=form, title=u'Ajouter une séquence')
