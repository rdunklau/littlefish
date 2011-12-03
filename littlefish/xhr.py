"""Views for xhr requests"""
from littlefish import app, db
from littlefish.utils import storify
from sqlalchemy.sql import func


@app.route('/xhr/suggest/<string:entity>/<string:attribute>')
def suggest(entity, attribute):
    """Suggest values from an array attribute of an entity"""
    entity = getattr(db, entity)
    return storify(db.db.session.query(func.unnest(getattr(entity, attribute))
            .label('label'))
            .distinct().all(),
            'label', 'label')
