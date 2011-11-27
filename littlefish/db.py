from flaskext.sqlalchemy import SQLAlchemy

from sqlalchemy.orm import relationship, backref


from . import app

db = SQLAlchemy()
db.init_app(app)
db.metadata.reflect(bind=db.get_engine(app))


def table(tablename):
    return db.metadata.tables[tablename]


class Seance(db.Model):
    __table__ = table('seance')
    sequence = relationship('Sequence', backref=backref('seances',
        lazy='joined'),
            lazy='joined')


class Sequence(db.Model):
    __table__ = table('sequence')
    topic_assoc = relationship('TopicDomainClass', backref=backref('sequences',
        lazy='joined'),
            lazy='joined')


class Etape(db.Model):
    __table__ = table('etape')
    seance = relationship('Seance', backref=backref('etapes', lazy='joined'),
            lazy='joined')

    @property
    def rowspan(self):
        return max(len(self.materiel_pe) + len(materiel_eleve),
                   len(self.dispositif),
                   len(self.deroulement))


class Class(db.Model):
    __table__ = table('class')


class Domain(db.Model):
    __table__ = table('domain')


class DomainClass(db.Model):
    __table__ = table('domain_class')
    domain = relationship(Domain, lazy='joined')
    grade = relationship(Class, lazy='joined')


class Topic(db.Model):
    __table__ = table('topic')


class TopicDomainClass(db.Model):
    __table__ = table('topic_domain_class')
    domain_class = relationship(DomainClass,
        lazy='joined',
        primaryjoin=(
            (__table__.c.class_code == table('domain_class').c.class_code) &
            (__table__.c.domain_code == table('domain_class').c.domain_code)))
    topic = relationship('Topic', lazy='joined')
    grade = relationship('Class', lazy='joined')
    domain = relationship('Domain', lazy='joined')
