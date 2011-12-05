"""Various utils"""
from flask import jsonify

from sqlalchemy.orm.collections import InstrumentedList
from sqlalchemy.orm import object_mapper
from sqlalchemy.orm.properties import ColumnProperty, RelationProperty
from sqlalchemy.sql import and_, func

from littlefish.db import db


def to_dict(item):
    """Transform a named tuple to a dict."""
    return {key: getattr(item, key) for key in item.keys()}


def storify(result, identifier='id', label='label'):
    """Returns a dojo itemfilereadstore suitable repr of a list of named
    tuples."""
    return jsonify({'items': [to_dict(item) for item in result],
                    'identifier': identifier,
                    'label': label})


def copy_entity(entity, visited=None):
    """Copy recursively an entity"""
    visited = visited or {}
    if entity in visited:
        return visited[entity]
    new_entity = entity.__class__()
    visited[entity] = new_entity
    for prop in object_mapper(entity).iterate_properties:
        if isinstance(prop, ColumnProperty):
            if not any([column.primary_key for column in prop.columns]):
                setattr(new_entity, prop.key, getattr(entity, prop.key))
    return new_entity


def move(entity, direction, lookup_key):
    clazz = entity.__class__
    lookup_value = getattr(entity, lookup_key)
    lookup_attr = getattr(clazz, lookup_key)
    pkey = object_mapper(entity).primary_key[0].key
    if direction == 'up':
        if entity.ordinal != 1:
            cond = clazz.ordinal == (entity.ordinal - 1)
            values = {clazz.ordinal: entity.ordinal}
            entity.ordinal = entity.ordinal - 1
    else:
        max_ordinal = (db.session.query(func.max(clazz.ordinal))
                    .filter(lookup_attr == lookup_value)
                    .scalar())
        if entity.ordinal < max_ordinal:
            cond = clazz.ordinal == (entity.ordinal + 1)
            values = {clazz.ordinal: entity.ordinal}
            entity.ordinal = entity.ordinal + 1
    if cond is not None and values:
        # Flush it now, so that it works
        db.session.flush()
        (clazz.query.filter(cond).filter(lookup_attr == lookup_value)
                .filter(getattr(clazz, pkey) != getattr(entity, pkey))
                .update(values))
