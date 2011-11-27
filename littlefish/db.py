from flaskext.sqlalchemy import SQLAlchemy

from sqlalchemy.orm import relationship


from . import app

db = SQLAlchemy()
db.init_app(app)
db.metadata.reflect(bind=db.get_engine(app))


def table(tablename):
    return db.metadata.tables[tablename]


class Seance(db.Model):
    __table__ = table('seance')
    sequence = relationship('Sequence', backref='seances')


class Sequence(db.Model):
    __table__ = table('sequence')
    topic_assoc = relationship('TopicDomainClass', backref='sequences')


class Etape(db.Model):
    __table__ = table('etape')
    seance = relationship('Seance', backref='etapes')


class Class(db.Model):
    __table__ = table('class')


class Domain(db.Model):
    __table__ = table('domain')


class DomainClass(db.Model):
    __table__ = table('domain_class')
    domain = relationship(Domain)
    grade = relationship(Class)


class Topic(db.Model):
    __table__ = table('topic')


class TopicDomainClass(db.Model):
    __table__ = table('topic_domain_class')
    domain_class = relationship(DomainClass,
        primaryjoin=(
            (__table__.c.class_code == table('domain_class').c.class_code) &
            (__table__.c.domain_code == table('domain_class').c.domain_code)))
    topic = relationship('Topic')
    grade = relationship('Class')
    domain = relationship('Domain')
