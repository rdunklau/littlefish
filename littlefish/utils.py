from flask import jsonify

def to_dict(item):
    return {key: getattr(item, key) for key in item.keys()}

def storify(result, identifier='id', label='label'):
    return jsonify({'items': [to_dict(item) for item in result],
                    'identifier': identifier,
                    'label': label})
