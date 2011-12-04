"""Various utils"""
from flask import jsonify
from sqlalchemy.orm.collections import InstrumentedList
from sqlalchemy.orm import object_mapper
from sqlalchemy.orm.properties import ColumnProperty, RelationProperty


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
