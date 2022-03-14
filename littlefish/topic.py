from flask import render_template, redirect, url_for, session, g, current_app
from flask.helpers import make_response
from flask_wtf import FlaskForm as Form, validators
from littlefish.db import (db, Class, Sequence, DomainClass, TopicDomainClass,
    Domain, Topic, Etape, Seance)


class TopicForm(Form):
	code = StringField(u'Code',  [validators.InputRequired()])
	label = StringField(u'Titre', [validators.InputRequired()])


@app.route('/topic/add/', methods=('GET', 'POST'))
def add_topic():
	form = TopicForm()
	if form.validate_on_submit():
        topic = Topic()
        form.populate_obj(topic)
        db.session.add(topic)
        db.session.commit()
        return redirect(url_for('topic', topic_id=topic.id), code=303)
	return render_template('wtforms/form.jinja2', form=form,
            title=u'Ajouter un thème', base_filter='')


