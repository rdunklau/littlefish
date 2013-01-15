# -*- coding: utf-8 -*-
"""Views managing a seance"""
from flask import render_template, redirect, url_for, g, session
from werkzeug.exceptions import Forbidden
from littlefish import app
from littlefish.db import db, Sequence, Seance
from littlefish.dojo import TextField, RichTextField
from littlefish.utils import move
from flaskext.wtf import Form, validators
from sqlalchemy.sql import func


class SeanceForm(Form):
    """A basic form for seance"""
    title = TextField(u'Titre', [validators.Required()])
    summary = RichTextField(u'Résumé')


@app.route('/seance/<int:seance_id>')
def seance(seance_id):
    """A single seance view"""
    seance_item = Seance.query.get_or_404(seance_id)
    g.breadcrumb = [(seance_item.sequence.title, url_for('sequence',
        sequence_id=seance_item.sequence_id))]
    return render_template('seance.html', seance=seance_item)


@app.route('/seance/<int:seance_id>/edit', methods=('GET', 'POST'))
def edit_seance(seance_id):
    """Edit seance view"""
    seance_item = Seance.query.get_or_404(seance_id)
    if seance_item.user_login != session['user']:
      raise Forbidden()
    g.breadcrumb = [(seance_item.sequence.title, url_for('sequence',
        sequence_id=seance_item.sequence_id)),
        (seance_item.title, url_for('seance', seance_id=seance_id))]
    form = SeanceForm(obj=seance_item)
    if form.validate_on_submit():
        form.populate_obj(seance_item)
        db.session.add(seance_item)
        db.session.commit()
        return redirect(url_for('seance', seance_id=seance_id), code=303)
    return render_template('wtforms/form.jinja2', form=form,
        title=u'Editer la séance %s' % seance_item.title)


@app.route('/seance/add/<int:sequence_id>', methods=('GET', 'POST'))
def add_seance(sequence_id):
    """Add seance view"""
    form = SeanceForm()
    seq = Sequence.query.get_or_404(sequence_id)
    if seq.user_login != session['user']:
      raise Forbidden()

    g.breadcrumb = [(seq.title, url_for('sequence',
        sequence_id=sequence_id))]
    if form.validate_on_submit():
        seance_item = Seance()
        seance_item.user_login = session['user']
        seance_item.sequence_id = sequence_id
        form.populate_obj(seance_item)
        seance_item.ordinal = (db.session.query(func.max(Seance.ordinal) +
                1).filter(Seance.sequence_id == sequence_id)
                .scalar()) or 1
        db.session.add(seance_item)
        db.session.commit()
        return redirect(url_for('sequence', sequence_id=sequence_id), code=303)
    return render_template('wtforms/form.jinja2', form=form,
            title=u'Ajouter une séance')


@app.route('/seance/<int:seance_id>/move/<any(up, down):direction>')
def move_seance(seance_id, direction):
    seance = Seance.query.get_or_404(seance_id)
    if seance.user_login != session['user']:
      raise Forbidden()
    move(seance, direction, 'sequence_id')
    db.session.commit()
    return redirect(url_for('sequence', sequence_id=seance.sequence_id),
            code=303)
