# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, request, session, g
from littlefish import app
from littlefish.db import db, Class, Sequence, DomainClass, TopicDomainClass,\
    Domain, Topic, Seance
from littlefish.dojo import TextField, SelectField, TreeField, TreeLevel,\
    ListField
from littlefish.utils import storify
from flaskext.wtf import Form, validators
from sqlalchemy.sql import func


class SeanceForm(Form):
    title = TextField(u'Titre', [validators.Required()])


@app.route('/seance/<int:seance_id>')
def seance(seance_id):
    seance = Seance.query.get_or_404(seance_id)
    g.breadcrumb = [(seance.sequence.title, url_for('sequence',
        sequence_id=seance.sequence_id))]
    return render_template('seance.html', seance=seance)


@app.route('/seance/<int:seance_id>/edit', methods=('GET', 'POST'))
def edit_seance(seance_id):
    seance = Seance.query.get_or_404(seance_id)
    g.breadcrumb = [(seance.sequence.title, url_for('sequence',
        sequence_id=seance.sequence_id)),
        (seance.title, url_for('seance', seance_id=seance_id))]
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
    seq = Sequence.query.get_or_404(sequence_id)
    g.breadcrumb = [(seq.title, url_for('sequence',
        sequence_id=sequence_id))]
    if form.validate_on_submit():
        seance = Seance()
        seance.sequence_id = sequence_id
        form.populate_obj(seance)
        ordinal = (db.session.query(func.max(Seance.ordinal) +
                1).filter(Seance.sequence_id == sequence_id)
                .scalar()) or 1
        db.session.add(seance)
        db.session.commit()
        return redirect(url_for('sequence', sequence_id=sequence_id), code=303)
    return render_template('wtforms/form.jinja2', form=form,
            title=u'Ajouter une séance')
