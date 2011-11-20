# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for
from littlefish import app
from littlefish.db import db, Class, Sequence


from flaskext.wtf import Form, SelectField, TextField, validators


class SequenceForm(Form):
    title = TextField(u'Titre', [validators.Required()])
    grade = SelectField(u'Classe', [validators.Required()])
    domain = SelectField(u'Domaine disciplinaire', [validators.Required()])
    topic = SelectField(u'Discipline', [validators.Required()])

@app.route('/sequence/<int:sequence_id>')
def sequence(sequence_id):
    seq = Sequence.query.get_or_404(sequence_id)
    return render_template('sequence.html')


@app.route('/sequence/add/', methods=('GET', 'POST'))
def add_sequence():
    classes = Class.query.all()
    form = SequenceForm()
    form.grade.choices = [(grade.code, grade.label) for grade in classes]
    form.domain.choices = [('', 'Choisir...')]
    form.topic.choices = [('', 'Choisir...')]
    if form.validate_on_submit():
        seq = Sequence()
        form.populate_obj(seq)
        db.session.add(seq)
        db.session.commit()
        return redirect(url_for('sequence', sequence_id=seq.id), code=303)
    return render_template('form.html', form=form, title=u'Ajouter une séquence')
