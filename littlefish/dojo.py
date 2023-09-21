# -*- coding: utf-8 -*-
"""Dojo support for WTForms"""
import json

from flask import render_template, request
import flask_wtf

from wtforms import widgets as wtfwidgets
from wtforms import fields as wtffields
from wtforms import validators
from markupsafe import Markup

import datetime


class DojoInput(wtfwidgets.Input):
    """Base class for dojo-based inputs"""

    __template__ = 'wtforms/input.jinja2'

    def __call__(self, field, **kwargs):
        attrs = {}
        attrs.setdefault('id', field.id)
        attrs.setdefault('type', self.input_type)
        attrs.setdefault('dojoType', self.dojo_type)
        attrs.setdefault('name', field.name)
        attrs.setdefault('value', field.data)
        attrs.update(kwargs.pop('options', {}))
        for validator in field.validators:
            if isinstance(validator, validators.InputRequired):
                attrs['required'] = 'required'
        return Markup(render_template(self.__template__,
            attrs=attrs, **kwargs))


class TextInput(wtfwidgets.TextInput, DojoInput):
    """A simple text input"""

    dojo_type = 'dijit.form.ValidationTextBox'


class StringField(wtffields.StringField):
    """Field associated with textinput"""

    widget = TextInput()


class PasswordInput(TextInput, DojoInput):
    """A simple text input"""

    dojo_type = 'dijit.form.TextBox'
    input_type = 'password'



class PasswordField(wtffields.PasswordField):
    """Field associated with textinput"""
    widget = PasswordInput()


class RichTextInput(TextInput, DojoInput):
    """A simple text input"""

    dojo_type = 'dijit.form.Textarea'


class RichStringField(wtffields.StringField):
    """Field associated with richtextinput"""

    widget = RichTextInput()


class Select(wtfwidgets.TextInput, DojoInput):
    """A select with autocompletion"""

    dojo_type = 'dijit.form.FilteringSelect'
    __template__ = 'wtforms/select.jinja2'

    def __call__(self, field, **kwargs):
        return super(Select, self).__call__(field, choices=field.choices,
                **kwargs)


class SelectField(wtffields.SelectField):
    """Field associated with Select"""

    widget = Select()


class TreeLevel(object):
    """A level in a tree select"""

    def __init__(self, label='', url='', required=True):
        self.label = label
        self.url = url
        self.required = required


class TreeSelect(wtfwidgets.TextInput, DojoInput):
    """A widget allowign to nest dependent selects, filtering their inputs"""

    def render(self, level, id, name, parent=None, value=None):
        """Utility method for endering a level"""
        attrs = {}
        attrs['id'] = id
        attrs['name'] = name
        attrs['data-datastore-url'] = level.url
        attrs['data-treeselect'] = True
        attrs['value'] = value
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
            html_string += self.render(level, id, name, parent,
                    value=field.levels_values[idx])
        level = field.levels[-1]
        parent = '%s-level%i' % (field.id, idx)
        html_string += self.render(level, field.id, field.name, parent,
                value=field.levels_values[-1])
        return Markup(html_string)


class TreeField(wtffields.StringField):
    """Field associated with the TreeSelect"""

    widget = TreeSelect()

    def __init__(self, *args, **kwargs):
        self.levels = kwargs.pop('levels')
        self.levels_values = [None for i in range(len(self.levels))]
        super(TreeField, self).__init__(*args, **kwargs)

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = valuelist[0]
            self.levels_values = []
            for idx in range(len(self.levels) - 1):
                self.levels_values.append(request.form.get('%s-level%i' % (
                    self.name, idx)))
            self.levels_values.append(self.data)


class ListInput(RichTextInput):
    """A dynamically sized list of suggest box inputs"""

    def __call__(self, field, **kwargs):
        attrs = {}
        attrs['id'] = field.id
        attrs['name'] = field.name
        attrs['data-datastore-url'] = field.url
        if field.base_filter:
            attrs['data-basefilter'] = field.base_filter
        return Markup(render_template('wtforms/list.jinja2',
            attrs=attrs, values=field.data or [], **kwargs))


class ListField(wtffields.StringField):
    """The field associated to the ListInput"""

    widget = ListInput()

    def __init__(self, *args, **kwargs):
        self.url = kwargs.pop('url')
        self.base_filter = kwargs.pop('base_filter', False)
        super(ListField, self).__init__(*args, **kwargs)

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = filter(lambda x: x, valuelist)
        else:
            self.data = []


class TimeInput(wtfwidgets.TextInput, DojoInput):
    """A time selector widget"""

    dojo_type = 'dijit.form.ValidationTextBox'

    def __call__(self, field, **kwargs):
        if field.data:
            total = field.data.total_seconds()
            div, mod = divmod(total, 3600)
            value = '%sh%02imin' % (int(div), int(mod / 60))
        else:
            value = '0h00min'
        kwargs['options'] = {
                'regExp': '(\d*h)?((\d\d)(min)?)?',
                'promptMessage': 'Format: 25min, ou 1h05min',
                'invalidMessage': u'Doit être une heure valide',
                'value': value
                }
        return super(TimeInput, self).__call__(field, **kwargs)


class TimeField(wtffields.StringField):
    """The field associated with the TimeInput"""

    widget = TimeInput()

    def process_formdata(self, valuelist):
        if valuelist:
            value = valuelist[0]
            value = value.replace('min', '')
            if 'h' in value:
                hour, minute = value.split('h')
            else:
                hour = 0
                minute = int(value)
            hour = int(hour)
            minute = int(minute)
            self.data = datetime.timedelta(hours=hour, minutes=minute)

    def process_data(self, value):
        self.data = value
