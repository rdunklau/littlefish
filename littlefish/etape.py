# -*- coding: utf-8 -*-
"""Views for managing an etape"""

from flask import render_template, redirect, url_for, request, session, g
from littlefish import app
from littlefish.db import db, Class, Seance, DomainClass, TopicDomainClass,\
    Domain, Topic, Etape
from littlefish.dojo import TextField, SelectField, TreeField, TreeLevel,\
    ListField, TimeField
from littlefish.utils import storify
from flaskext.wtf import Form, validators
from sqlalchemy.sql import func


class EtapeForm(Form):
    """The form  defining an etape"""
    title = TextField(u'Titre', [validators.Required()])
    time = TimeField(u'Durée')
    objectif = TextField(u'Objectif', [validators.Required()])
    dispositif = ListField(u'Dispositif', url='/xhr/suggest/Etape/dispositif')
    deroulement = ListField(u'Déroulement',
            url='/xhr/suggest/Etape/deroulement')
    materiel_pe = ListField(u'Matériel PE',
            url='/xhr/suggest/Etape/materiel_pe')
    materiel_eleve = ListField(u'Matériel élève',
            url='/xhr/suggest/Etape/materiel_eleve')
    consignes_criteres = ListField(u'Consignes / Critères',
            url='/xhr/suggest/Etape/consignes_criteres')
    pe_role = ListField(u'Rôle PE', url='/xhr/suggest/Etape/pe_role')


@app.route('/etape/<int:seance_id>/<int:ordinal>')
def etape(seance_id, ordinal):
    """View presenting an etape itself"""
    return render_template('etape.html')


@app.route('/etape/<int:seance_id>/<int:ordinal>/edit',
        methods=('GET', 'POST'))
def edit_etape(seance_id, ordinal):
    """Edit etape view"""
    etape = Etape.query.filter_by(seance_id=seance_id, ordinal=ordinal).one()
    seq = etape.seance.sequence
    g.breadcrumb = [(seq.title, url_for('sequence',
        sequence_id=etape.seance.sequence_id)),
        (etape.seance.title, url_for('seance', seance_id=seance_id))]
    form = EtapeForm(obj=etape)
    if form.validate_on_submit():
        form.populate_obj(etape)
        db.session.add(etape)
        db.session.commit()
        return redirect(url_for('seance', seance_id=seance_id), code=303)
    return render_template('wtforms/form.jinja2', form=form,
        title=u"Editer l'étape %s" % etape.ordinal)


@app.route('/etape/add/<int:seance_id>', methods=('GET', 'POST'))
def add_etape(seance_id):
    """Add etape view"""
    form = EtapeForm()
    seance = Seance.query.get_or_404(seance_id)
    g.breadcrumb = [(seance.sequence.title, url_for('sequence',
        sequence_id=seance.sequence_id)),
        (seance.title, url_for('seance', seance_id=seance_id))]
    if form.validate_on_submit():
        etape = Etape()
        ordinal = (db.session.query(func.max(Etape.ordinal) +
                1).filter(Etape.seance_id == seance_id)
                .scalar()) or 1
        etape.ordinal = ordinal
        etape.seance_id = seance_id
        form.populate_obj(etape)
        db.session.add(etape)
        db.session.commit()
        return redirect(url_for('seance', seance_id=seance_id), code=303)
    return render_template('wtforms/form.jinja2', form=form,
            title=u'Ajouter une étape')
