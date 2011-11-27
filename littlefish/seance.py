# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, request, session
from littlefish import app
from littlefish.db import db, Class, Sequence, DomainClass, TopicDomainClass,\
    Domain, Topic, Seance
from littlefish.dojo import TextField, SelectField, TreeField, TreeLevel,\
    ListField
from littlefish.utils import storify
from flaskext.wtf import Form, validators


class SeanceForm(Form):
    title = TextField(u'Titre', [validators.Required()])


@app.route('/seance/<int:seance_id>')
def seance(seance_id):
    return render_template('seance.jinja2')


@app.route('/seance/<int:seance_id>/edit', methods=('GET', 'POST'))
def edit_seance(seance_id):
    seance = Seance.query.get_or_404(seance_id)
    form = SeanceForm(obj=seq)
    if form.validate_on_submit():
        form.populate_obj(seance)
        db.session.add(seq)
        db.session.commit()
        return redirect(url_for('seance', seance_id=seq.id), code=303)
    return render_template('wtforms/form.jinja2', form=form,
        title=u'Editer la séance %s' % seq.title)


@app.route('/seance/add/<int:sequence_id>', methods=('GET', 'POST'))
def add_seance(sequence_id):
    form = SeanceForm()
    if form.validate_on_submit():
        seance = Seance()
        seance.sequence_id = sequence_id
        form.populate_obj(seance)
        db.session.add(seance)
        db.session.commit()
        return redirect(url_for('sequence', sequence_id=seq.id), code=303)
    return render_template('wtforms/form.jinja2', form=form,
            title=u'Ajouter une séance')
