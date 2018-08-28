"""SQLAlchemy entities definition"""
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import Column
from sqlalchemy.orm import relationship, backref


from . import app

db = SQLAlchemy()
db.init_app(app)
db.metadata.reflect(bind=db.get_engine(app))


def table(tablename):
    """Helper to get a table by name"""
    return db.metadata.tables[tablename]


class Sequence(db.Model):
    """Central entity in the application.
    Is linked to a topic, a domain and a class via the topic_domain_class
    table.
    """
    __table__ = table('sequence')
    topic_assoc = relationship('TopicDomainClass', backref=backref('sequences',
        lazy='joined'),
            lazy='joined')
    user = relationship('User')
    copy_of = relationship('Sequence', uselist=False)


class Seance(db.Model):
    """A Seance is the second level of organization, below Sequence"""
    __table__ = table('seance')
    sequence = relationship('Sequence', backref=backref('seances',
        lazy='joined', order_by='Seance.ordinal'),
            lazy='joined')
    topic_assoc = relationship('TopicDomainClass',
            secondary='sequence')
    user = relationship('User')
    copy_of = relationship('Seance', uselist=False)

class Etape(db.Model):
    """An Etape is the third level of organization"""
    __table__ = table('etape')
    seance = relationship('Seance', backref=backref('etapes', lazy='joined',
        order_by='Etape.ordinal'),
            lazy='joined')
    user = relationship('User')
    copy_of = relationship('Etape', uselist=False)

class Class(db.Model):
    """A class (eg, CM1, CM2..)"""
    __table__ = table('class')


class Domain(db.Model):
    """A study domain (french, mathematics...)"""
    __table__ = table('domain')


class DomainClass(db.Model):
    """Association between domains and classes"""
    __table__ = table('domain_class')
    domain = relationship(Domain, lazy='joined')
    grade = relationship(Class, lazy='joined')



class Topic(db.Model):
    """A specific topic."""
    __table__ = table('topic')
    topic = relationship('Topic', remote_side=[__table__.c.code])

    @property
    def path(self):
        parts = []
        if self.topic is not None:
            parts.extend(self.topic.path)
        parts.append(self.label)
        return parts

        
            

class TopicDomainClass(db.Model):
    """Associates a topic to a domain and class"""
    __table__ = table('topic_domain_class')
    domain_class = relationship(DomainClass,
        lazy='joined',
        primaryjoin=(
            (__table__.c.class_code == table('domain_class').c.class_code) &
            (__table__.c.domain_code == table('domain_class').c.domain_code)))
    topic = relationship('Topic', lazy='joined')
    grade = relationship('Class', lazy='joined')
    domain = relationship('Domain', lazy='joined')

class User(db.Model):
  """A user from the application."""
  __table__ = table('user')

  @property
  def fullname(self):
    return "%s %s" % (self.firstname.capitalize(),
                      self.lastname.capitalize())
