"""Various utils"""
from flask import jsonify


def to_dict(item):
    """Transform a named tuple to a dict."""
    return {key: getattr(item, key) for key in item.keys()}


def storify(result, identifier='id', label='label'):
    """Returns a dojo itemfilereadstore suitable repr of a list of named
    tuples."""
    return jsonify({'items': [to_dict(item) for item in result],
                    'identifier': identifier,
                    'label': label})
