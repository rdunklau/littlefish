drop database littlefish;
create database littlefish with owner littlefish;

\connect littlefish littlefish

create table class (
    code character varying primary key,
    label character varying not null
);

insert into class (code, label) VALUES
	('TPS', 'Toute Petite Section'),
	('PS', 'Petite Section'),
	('MS', 'Moyenne Section'),
	('GS', 'Grande Section'),
    ('CP', 'Cours Préparatoire'),
    ('CE1', 'Cours Élémentaire 1'),
    ('CE2', 'Cours Élementaire 2'),
    ('CM1', 'Cours Moyen 1'),
    ('CM2', 'Cours Moyen 2');


create table domain (
	code character varying primary key,
	label character varying not null
);


insert into domain (code, label) values
	('FRANCAIS', 'Français'), 
	('MATHS', 'Mathématiques'), 
	('EPS', 'EPS'),
	('LV', 'Langue Vivante'),
	('SET', 'Sciences expérimentales et technologies'), 
	('CHU', 'Culture Humaniste'),
	('DEC', 'Découverte du monde'), 
	('PAHA', 'Pratique artistique et histoire des arts'),
	('APL', E'S\'approprier le langage'),
	('DE', E'Découvrir l\'écrit'),
	('DEV', 'Devenir élève'),
	('AEC', E'Agir et s\'exprimer avec son corps'),
	('DMP', E'Découvrir le monde proche'),
	('PSIC', 'Percevoir, Sentir, Imaginer, Créer');


create table domain_class (
  id serial primary key,
  class_code character varying references class(code),
  domain_code character varying references domain(code),
  unique (class_code, domain_code)
);

insert into domain_class (class_code, domain_code)  VALUES
  ('TPS', 'APL'),
  ('TPS', 'DE'),
  ('TPS', 'DEV'),
  ('TPS', 'AEC'),
  ('TPS', 'DMP'),
  ('TPS', 'PSIC'),
  ('PS', 'APL'),
  ('PS', 'DE'),
  ('PS', 'DEV'),
  ('PS', 'AEC'),
  ('PS', 'DMP'),
  ('PS', 'PSIC'),
  ('MS', 'APL'),
  ('MS', 'DE'),
  ('MS', 'DEV'),
  ('MS', 'AEC'),
  ('MS', 'DMP'),
  ('MS', 'PSIC'),
  ('GS', 'APL'),
  ('GS', 'DE'),
  ('GS', 'DEV'),
  ('GS', 'AEC'),
  ('GS', 'DMP'),
  ('GS', 'PSIC'),
  ('CP', 'FRANCAIS'),
  ('CP', 'MATHS'),
  ('CP', 'EPS'),
  ('CP', 'LV'),
  ('CP', 'PAHA'),
  ('CP', 'DEC'),
  ('CE1', 'FRANCAIS'),
  ('CE1', 'MATHS'),
  ('CE1', 'EPS'),
  ('CE1', 'LV'),
  ('CE1', 'PAHA'),
  ('CE1', 'DEC'),
  ('CE2', 'FRANCAIS'),
  ('CE2', 'MATHS'),
  ('CE2', 'EPS'),
  ('CE2', 'LV'),
  ('CE2', 'SET'),
  ('CE2', 'CHU'),
  ('CM1', 'FRANCAIS'),
  ('CM1', 'MATHS'),
  ('CM1', 'EPS'),
  ('CM1', 'LV'),
  ('CM1', 'SET'),
  ('CM1', 'CHU'),
  ('CM2', 'FRANCAIS'),
  ('CM2', 'MATHS'),
  ('CM2', 'EPS'),
  ('CM2', 'LV'),
  ('CM2', 'SET'),
  ('CM2', 'CHU');


create table topic (
  code character varying primary key,
  label character varying
);

create table topic_domain_class (
  id serial primary key,
  class_code character varying,
  domain_code character varying,
  topic_code character varying,
  unique (class_code, domain_code, topic_code),
  foreign key (class_code, domain_code) references domain_class(class_code, domain_code),
  foreign key (class_code) references class(code),
  foreign key (domain_code) references domain(code),
  foreign key (topic_code) references topic(code)
);


insert into topic (code, label)  VALUES
  ('FRANCAIS_LO', 'Langage oral'),
  ('FRANCAIS_LECTURE', 'Lecture'),
  ('FRANCAIS_ECRITURE', 'Ecriture'),
  ('FRANCAIS_VOCAB', 'Vocabulaire'),
  ('FRANCAIS_GRAMMAIRE', 'Grammaire'),
  ('FRANCAIS_ORTHO', 'Orthographe'),
  ('FRANCAIS_LITTERATURE', 'Littérature'),
  ('FRANCAIS_REDACTION', 'Rédaction');

INSERT INTO topic_domain_class (class_code, domain_code, topic_code) VALUES 
	('CP', 'FRANCAIS', 'FRANCAIS_LO'),
	('CE1', 'FRANCAIS', 'FRANCAIS_LO'),
	('CE2', 'FRANCAIS', 'FRANCAIS_LO'),
	('CM1', 'FRANCAIS', 'FRANCAIS_LO'),
	('CM2', 'FRANCAIS', 'FRANCAIS_LO'),
	('CP', 'FRANCAIS', 'FRANCAIS_LECTURE'),
	('CE1', 'FRANCAIS', 'FRANCAIS_LECTURE'),
	('CE2', 'FRANCAIS', 'FRANCAIS_LECTURE'),
	('CM1', 'FRANCAIS', 'FRANCAIS_LECTURE'),
	('CM2', 'FRANCAIS', 'FRANCAIS_LECTURE'),
	('CP', 'FRANCAIS', 'FRANCAIS_ECRITURE'),
	('CE1', 'FRANCAIS', 'FRANCAIS_ECRITURE'),
	('CE2', 'FRANCAIS', 'FRANCAIS_ECRITURE'),
	('CM1', 'FRANCAIS', 'FRANCAIS_ECRITURE'),
	('CM2', 'FRANCAIS', 'FRANCAIS_ECRITURE'),
	('CP', 'FRANCAIS', 'FRANCAIS_VOCAB'),
	('CE1', 'FRANCAIS', 'FRANCAIS_VOCAB'),
	('CE2', 'FRANCAIS', 'FRANCAIS_VOCAB'),
	('CM1', 'FRANCAIS', 'FRANCAIS_VOCAB'),
	('CM2', 'FRANCAIS', 'FRANCAIS_VOCAB'),
	('CP', 'FRANCAIS', 'FRANCAIS_GRAMMAIRE'),
	('CE1', 'FRANCAIS', 'FRANCAIS_GRAMMAIRE'),
	('CE2', 'FRANCAIS', 'FRANCAIS_GRAMMAIRE'),
	('CM1', 'FRANCAIS', 'FRANCAIS_GRAMMAIRE'),
	('CM2', 'FRANCAIS', 'FRANCAIS_GRAMMAIRE'),
	('CP', 'FRANCAIS', 'FRANCAIS_ORTHO'),
	('CE1', 'FRANCAIS', 'FRANCAIS_ORTHO'),
	('CE2', 'FRANCAIS', 'FRANCAIS_ORTHO'),
	('CM1', 'FRANCAIS', 'FRANCAIS_ORTHO'),
	('CM2', 'FRANCAIS', 'FRANCAIS_ORTHO'),
	('CE2', 'FRANCAIS', 'FRANCAIS_LITTERATURE'),
	('CM1', 'FRANCAIS', 'FRANCAIS_LITTERATURE'),
	('CM2', 'FRANCAIS', 'FRANCAIS_LITTERATURE'),
	('CE2', 'FRANCAIS', 'FRANCAIS_REDACTION'),
	('CM1', 'FRANCAIS', 'FRANCAIS_REDACTION'),
	('CM2', 'FRANCAIS', 'FRANCAIS_REDACTION');


  




create table sequence_attrs (
  	code character varying primary key,
	label character varying
);

insert into sequence_attrs(code, label) VALUES
	('DECOUVERTE', 'Découverte'),
	('RECHERCHE', 'Recherche/Manipulation'),
	('REINVESTISSEMENT', 'Réinvestissement'),
	('EVALUATION', 'Évaluation');

create table sequence (
    id serial primary key,
    title character varying not null,
	topic_domain_class integer references topic_domain_class(id),
	programmes character varying[],
	socles character varying[],
	prerequis character varying[],
	competences character varying[],
	objectifs character varying[],
	taches character varying[],
	roles character varying[],
	materiel_pe character varying[],
	materiel_eleve character varying[],
    period integer
);


create table seance (
    id serial primary key,
    sequence integer references sequence(id),
    title character varying
);


create table etape (
    ordinal integer,
    seance integer references seance(id),
    time interval,
    description character varying,
    succeed_criteria character varying,
    pe_role character varying,
    primary key (ordinal, seance)
);

