# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, request, session, g
from littlefish import app
from littlefish.db import db, Class, Sequence, DomainClass, TopicDomainClass,\
    Domain, Topic
from littlefish.dojo import TextField, SelectField, TreeField, TreeLevel,\
    ListField
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
        .filter(Class.code == session['classe'])
        .all())


@app.route('/sequence/xhr/Topic')
def topic_select():
    return storify(db.session.query(TopicDomainClass.id,
            Topic.label,
            DomainClass.id.label('parent'))
        .select_from(TopicDomainClass)
        .join(DomainClass)
        .join(Class)
        .filter(Class.code == session['classe'])
        .join(Topic)
        .all())


class SequenceForm(Form):
    title = TextField(u'Titre', [validators.Required()])
    topic_domain_class = TreeField(u'Niveau/Discipline', levels=[
        TreeLevel('Domaine Disciplinaire', '/sequence/xhr/Domain'),
        TreeLevel('Discipline', '/sequence/xhr/Topic')])
    programmes = ListField('Programmes',
            url='/xhr/suggest/Sequence/programmes')
    socles = ListField('Socles communs',
            url='/xhr/suggest/Sequence/socles')
    prerequis = ListField(u'Prérequis',
            url='/xhr/suggest/Sequence/prerequis')
    competences = ListField(u'Compétences',
            url='/xhr/suggest/Sequence/competences')
    objectifs = ListField(u'Objectifs',
            url='/xhr/suggest/Sequence/objectifs')
    taches = ListField(u'Tâches',
            url='/xhr/suggest/Sequence/taches')
    roles = ListField(u'Rôles',
            url='/xhr/suggest/Sequence/roles')
    materiel_pe = ListField(u'Matériel PE',
            url='/xhr/suggest/Sequence/materiel_pe')
    materiel_eleve = ListField(u'Matériel élève',
            url='/xhr/suggest/Sequence/materiel_eleve')


@app.route('/sequence/<int:sequence_id>')
def sequence(sequence_id):
    seq = Sequence.query.get_or_404(sequence_id)
    return render_template('sequence.html', sequence=seq)


@app.route('/sequence/<int:sequence_id>/edit', methods=('GET', 'POST'))
def edit_sequence(sequence_id):
    seq = Sequence.query.get_or_404(sequence_id)
    g.breadcrumb = [(seq.title, url_for('sequence', sequence_id=sequence_id))]
    form = SequenceForm(obj=seq)
    if form.validate_on_submit():
        form.populate_obj(seq)
        prog = request.values.getlist('programmes')
        db.session.add(seq)
        db.session.commit()
        return redirect(url_for('sequence', sequence_id=seq.id), code=303)
    form.topic_domain_class.levels_values = [
            seq.topic_assoc.domain_class.id,
            seq.topic_assoc.id]
    return render_template('wtforms/form.jinja2', form=form,
        title=u'Editer la séquence %s' % seq.title)


@app.route('/sequence/add/', methods=('GET', 'POST'))
def add_sequence():
    form = SequenceForm()
    if form.validate_on_submit():
        seq = Sequence()
        form.populate_obj(seq)
        prog = request.values.getlist('programmes')
        db.session.add(seq)
        db.session.commit()
        return redirect(url_for('sequence', sequence_id=seq.id), code=303)
    return render_template('wtforms/form.jinja2', form=form,
            title=u'Ajouter une séquence')
