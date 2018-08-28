"""Views for xhr requests"""
from flask import request, session
from littlefish import app
from littlefish.db import Sequence, TopicDomainClass, Seance, Etape, db
from littlefish.utils import storify
from sqlalchemy.sql import func


@app.route('/xhr/suggest/Sequence/<string:attribute>')
def suggest_sequence(attribute):
    """Suggest values from an array attribute of an entity"""
    entity = Sequence
    query = (db.session.query(func.unnest(getattr(entity, attribute))
            .label('label'))
            .distinct()
            .filter(entity.auto_suggest == True)
            .filter(entity.user_login == session['user']))
    if request.values:
        query = query.join(TopicDomainClass)
        for key, value in request.values.items():
            query = query.filter(getattr(TopicDomainClass, key) == value)
    return storify(query.all(),
            'label', 'label')


@app.route('/xhr/suggest/Etape/<string:attribute>')
def suggest_etape(attribute):
    """Suggest values from an array attribute of an entity"""
    entity = Etape
    query = (db.session.query(func.unnest(getattr(entity, attribute))
            .label('label'))
            .distinct()
            .filter(entity.auto_suggest == True)
            .filter(entity.user_login == session['user']))
    if request.values:
        query = (query.join(Seance)
                    .join(Sequence)
                    .join(TopicDomainClass))
        for key, value in request.values.items():
            query = query.filter(getattr(TopicDomainClass, key) == value)
    return storify(query.all(),
            'label', 'label')
