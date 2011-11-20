from littlefish import app, db
from flask import request, jsonify
from sqlalchemy.sql import and_

def jsonify_entity(entity):
    pk = entity.__class__.__mapper__.primary_key_from_instance(entity)
    truc = db.db.session.bind
    grou = db.db.session.query(db.Topic).filter_by(code='FRANCAIS_REDACTION').one().label
    return {'id': pk[0],
            'label': entity.label.encode('utf8')}

@app.route('/xhr/<any(Domain, Topic):model>/')
def dependent_location(model):
    model = getattr(db, model)
    criteria = and_(*(getattr(model, key) == value 
        for key, value in request.values.items()))
    query = model.query
    if criteria is not None:
        query = query.filter(criteria)
    truc = query.all()
    return jsonify({'results': [jsonify_entity(result) 
        for result in query.all()]})
