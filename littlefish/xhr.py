from littlefish.db import Sequence, db
from littlefish import app
from littlefish.utils import storify
from flask import request, jsonify
from sqlalchemy.sql import and_, func


@app.route('/xhr/suggest/<string:attribute>')
def suggest(attribute):
    return storify(db.session.query(func.unnest(getattr(Sequence,
        func.unnest(attr).label('label')).distinct().all(), 'label', 'label')))
