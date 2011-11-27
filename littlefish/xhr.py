from littlefish import app, db
from littlefish.utils import storify
from flask import request, jsonify
from sqlalchemy.sql import and_, func


@app.route('/xhr/suggest/<string:entity>/<string:attribute>')
def suggest(entity, attribute):
    entity = getattr(db, entity)
    return storify(db.db.session.query(func.unnest(getattr(entity, attribute))
            .label('label'))
            .distinct().all(),
            'label', 'label')
