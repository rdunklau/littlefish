import json

from flask import render_template
from flaskext import wtf as flaskwtf

from wtforms import widgets as wtfwidgets
from wtforms import fields as wtffields
from wtforms import validators


class DojoInput(wtfwidgets.Input):

    __template__ = 'wtforms/input.jinja2'

    def __call__(self, field, **kwargs):
        attrs = {}
        attrs.setdefault('id', field.id)
        attrs.setdefault('type', self.input_type)
        attrs.setdefault('dojoType', self.dojo_type)
        attrs.setdefault('name', field.name)
        for validator in field.validators:
            if isinstance(validator, validators.Required):
                attrs['required'] = 'true'
        return wtfwidgets.HTMLString(render_template(self.__template__,
            attrs=attrs, **kwargs))


class TextInput(wtfwidgets.TextInput, DojoInput):

    dojo_type = 'dijit.form.ValidationTextBox'


class TextField(wtffields.TextField):

    widget = TextInput()


class Select(wtfwidgets.TextInput, DojoInput):

    dojo_type = 'dijit.form.FilteringSelect'
    __template__ = 'wtforms/select.jinja2'

    def __call__(self, field, **kwargs):
        return super(Select, self).__call__(field, choices=field.choices,
                **kwargs)

class SelectField(wtffields.SelectField):

    widget = Select()



class TreeLevel(object):

    def __init__(self, label='', url=''):
        self.label = label
        self.url = url
        

class TreeSelect(wtfwidgets.TextInput, DojoInput):

    def render(self, level, id, name, parent=None):
        attrs = {}
        attrs['id'] = id
        attrs['name'] = name
        attrs['data-datastore-url'] = level.url
        if parent is not None:
            attrs['data-parent'] = parent
        attrs['data-dojo-store'] = ('new dojo.data.ItemFileReadStore({url:'
                '"%s"});' % level.url)
        html_string = '<label for="%s">%s</label>' % (id, level.label)
        html_string += render_template('wtforms/treeselect.jinja2',
                attrs=attrs)
        return html_string

    
    def __call__(self, field, **kwargs):
        html_string = ''
        for idx, level in enumerate(field.levels[:-1]):
            attrs = {}
            id = '%s-level%i' % (field.id, idx)
            name = '%s-level%i' % (field.name, idx)
            if idx > 0:
                parent = '%s-level%i' % (field.id, idx - 1)
            else:
                parent = None
            html_string += self.render(level, id, name, parent)
        level = field.levels[-1]
        parent = '%s-level%i' % (field.id, idx)
        html_string += self.render(level, field.id, field.name, parent)
        return wtfwidgets.HTMLString(html_string)

        
class TreeField(wtffields.TextField):

    widget = TreeSelect()

    def __init__(self, *args, **kwargs):
        self.levels = kwargs.pop('levels')
        super(TreeField, self).__init__(*args, **kwargs)
