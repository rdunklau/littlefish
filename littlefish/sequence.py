# -*- coding: utf-8 -*-
"""Sequence views"""
from flask import render_template, redirect, url_for, session, g
from flask.helpers import make_response
from littlefish import app
from littlefish.db import (db, Class, Sequence, DomainClass, TopicDomainClass,
    Domain, Topic, Etape, Seance)
from littlefish.dojo import (TextField, TreeField, TreeLevel, ListField)
from littlefish.utils import storify, copy_entity
from sqlalchemy import func

from flaskext.wtf import Form, validators
import weasy
from StringIO import StringIO


@app.route('/sequence/xhr/Class/')
def classes_select():
    """JSON view of all the classes"""
    return storify(db.session.query(Class.code.label('id'), Class.label).all())


@app.route('/sequence/xhr/Domain')
def domain_select():
    """JSON view of the domains for current class"""
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
    """JSON view for all topic attached to the current class"""
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
    """Form for managing sequences"""
    title = TextField(u'Titre', [validators.Required()])
    topic_domain_class = TreeField(u'', levels=[
        TreeLevel('Domaine Disciplinaire', '/sequence/xhr/Domain'),
        TreeLevel('Discipline', '/sequence/xhr/Topic')])
    programmes = ListField('Programmes',
            url='/xhr/suggest/Sequence/programmes',
            base_filter='topic_domain_class')
    socles = ListField('Socle commun',
            url='/xhr/suggest/Sequence/socles')
    prerequis = ListField(u'Prérequis',
            url='/xhr/suggest/Sequence/prerequis',
            base_filter='topic_domain_class')
    competences = ListField(u'Compétences',
            url='/xhr/suggest/Sequence/competences',
            base_filter='topic_domain_class')
    objectifs = ListField(u'Objectifs',
            url='/xhr/suggest/Sequence/objectifs',
            base_filter='topic_domain_class')
    taches = ListField(u'Tâches',
            url='/xhr/suggest/Sequence/taches')
    roles = ListField(u'Rôles du PE',
            url='/xhr/suggest/Sequence/roles')
    materiel_pe = ListField(u'Matériel PE',
            url='/xhr/suggest/Sequence/materiel_pe')
    materiel_eleve = ListField(u'Matériel élève',
            url='/xhr/suggest/Sequence/materiel_eleve')


@app.route('/sequence/<int:sequence_id>')
def sequence(sequence_id):
    """Single sequence view"""
    seq = Sequence.query.get_or_404(sequence_id)
    return render_template('sequence.html', sequence=seq)


@app.route('/sequence/<int:sequence_id>/edit', methods=('GET', 'POST'))
def edit_sequence(sequence_id):
    """Edit sequence view"""
    seq = Sequence.query.get_or_404(sequence_id)
    g.breadcrumb = [(seq.title, url_for('sequence', sequence_id=sequence_id))]
    form = SequenceForm(obj=seq)
    if form.validate_on_submit():
        form.populate_obj(seq)
        db.session.add(seq)
        db.session.commit()
        return redirect(url_for('sequence', sequence_id=seq.id), code=303)
    form.topic_domain_class.levels_values = [
            seq.topic_assoc.domain_class.id,
            seq.topic_assoc.id]
    return render_template('wtforms/form.jinja2', form=form,
            title=u'Editer la séquence %s' % seq.title,
            base_filter='id=%s' % (seq.topic_assoc.id))


@app.route('/sequence/add/', methods=('GET', 'POST'))
def add_sequence():
    """Add sequence view"""
    form = SequenceForm()
    if form.validate_on_submit():
        seq = Sequence()
        form.populate_obj(seq)
        db.session.add(seq)
        db.session.commit()
        return redirect(url_for('sequence', sequence_id=seq.id), code=303)
    return render_template('wtforms/form.jinja2', form=form,
            title=u'Ajouter une séquence',
            base_filter='id=%s' % (seq.topic_assoc.id))


@app.route('/sequence/<int:sequence_id>/pdf')
def sequence_pdf(sequence_id):
    """PDF view of a sequence and its seances, etapes..."""
    seq = Sequence.query.get_or_404(sequence_id)
    materiel_pe = (db.session.query(
                    func.unnest(Etape.materiel_pe).label('materiel'))
                    .select_from(Sequence)
                    .join(Seance)
                    .join(Etape)
                    .filter(Sequence.id == seq.id)
                    .distinct()
                    .all())
    materiel_eleve = (db.session.query(
                    func.unnest(Etape.materiel_eleve).label('materiel'))
                    .select_from(Sequence)
                    .join(Seance)
                    .join(Etape)
                    .filter(Sequence.id == seq.id)
                    .distinct()
                    .all())
    materiel_pe = set([m.materiel for m in materiel_pe] + seq.materiel_pe)
    materiel_eleve = set([m.materiel for m in materiel_eleve] +
                        seq.materiel_eleve)
    html = render_template('print/sequence.jinja2', sequence=seq,
            materiel_pe=materiel_pe,
            materiel_eleve=materiel_eleve)
    pdf = weasy.PDFDocument.from_string(html)
    pdf_out = StringIO()
    pdf.write_to(pdf_out)
    response = make_response(pdf_out.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = \
            "attachemnt; filename=%s.pdf" % seq.title
    return response


@app.route('/sequence/<int:sequence_id>/pdfpreview')
def sequence_pdf_preview(sequence_id):
    """PDF view of a sequence and its seances, etapes..."""
    seq = Sequence.query.get_or_404(sequence_id)
    html = render_template('print/sequence.jinja2', sequence=seq)
    return html


@app.route('/sequence/<int:sequence_id>/copy/')
def copy_sequence(sequence_id):
    """Copy a sequence, and all its related objects"""
    seq = Sequence.query.get_or_404(sequence_id)
    newseq = copy_entity(seq)
    newseq.title = 'Copie de %s' % newseq.title
    db.session.add(newseq)
    for seance in seq.seances:
        newseance = copy_entity(seance)
        db.session.add(newseance)
        for etape in seance.etapes:
            newetape = copy_entity(etape)
            db.session.add(newetape)
            newseance.etapes.append(newetape)
        newseq.seances.append(newseance)
    db.session.commit()
    return redirect('/', code=303)
