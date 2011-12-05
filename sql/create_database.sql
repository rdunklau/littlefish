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
  ('FRANCAIS_REDACTION', 'Rédaction'),
  ('MATHS_NOMBRES', 'Nombres et calcul'),
  ('MATHS_GEOMETRIE', 'Géométrie'),
  ('MATHS_GRANDEUR', 'Grandeurs et mesures'),
  ('MATHS_ORGA', 'Organisation et gestion de données'),
  ('EPS_PERF', 'Réaliser une performance mesurée (en distance, en temps'),
  ('EPS_ADAPTER', 'Adapter ses déplacements à différents types d’environnement'),
  ('EPS_EQUIPE', 'Coopérer ou s’opposer individuellement et collectivement'),
  ('EPS_EXPRESSION', 'Concevoir et réaliser des actions à visées expressive, artistique, esthétique'),
  ('SET_MATIERE', 'La matière'),
  ('SET_ENERGIE', E'L’énergie'),
  ('SET_VIVANT_UNITE',  E'L’unité et la diversité du vivant'),
  ('SET_VIVANT_FONCTIONNEMENT', 'Le fonctionnement du vivant'),
  ('SET_CORPS_HUMAIN', 'Le fonctionnement du corps humain et la santé'),
  ('SET_VIVANT_ENVIRONNEMENT', 'Les êtres vivants dans leur environnement'),
  ('SET_TECHNO', 'Les objets techniques'),
  ('LV_COMPREHENSION', 'Compréhension'),
  ('LV_EXPRESSION', 'Expression'),
  ('LV_VOCABULAIRE', 'Vocabulaire'),
  ('LV_GRAMMAIRE', 'Grammaire'),
  ('CHU_HISTOIRE', 'Histoire'),
  ('CHU_GEO', 'Géographie'),
  ('CHU_ICM', 'Instruction civique et morale'),
  ('CHU_HISTART', 'Histoire des arts'),
  ('CHU_ARTVIS', 'Arts Visuels'),
  ('CHU_MUSIC', 'Éducation musicale');



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
	('CM2', 'FRANCAIS', 'FRANCAIS_REDACTION'),
	('CM1', 'MATHS', 'MATHS_NOMBRES'),
	('CM1', 'MATHS', 'MATHS_GEOMETRIE'),
	('CM1', 'MATHS', 'MATHS_GRANDEUR'),
	('CM1', 'MATHS', 'MATHS_ORGA'),
	('CM1', 'EPS', 'EPS_PERF'),
	('CM1', 'EPS', 'EPS_ADAPTER'),
	('CM1', 'EPS', 'EPS_EQUIPE'),
	('CM1', 'EPS', 'EPS_EXPRESSION'),
	('CM1', 'SET', 'SET_MATIERE'),
	('CM1', 'SET', 'SET_ENERGIE'),
	('CM1', 'SET', 'SET_VIVANT_UNITE'),
	('CM1', 'SET', 'SET_VIVANT_FONCTIONNEMENT'),
	('CM1', 'SET', 'SET_CORPS_HUMAIN'),
	('CM1', 'SET', 'SET_VIVANT_ENVIRONNEMENT'),
	('CM1', 'SET', 'SET_TECHNO'),
	('CM1', 'LV', 'LV_COMPREHENSION'),
	('CM1', 'LV', 'LV_EXPRESSION'),
	('CM1', 'LV', 'LV_VOCABULAIRE'),
	('CM1', 'LV', 'LV_GRAMMAIRE'),
	('CM1', 'CHU', 'CHU_HISTOIRE'),
	('CM1', 'CHU', 'CHU_GEO'),
	('CM1', 'CHU', 'CHU_ICM'),
	('CM1', 'CHU', 'CHU_HISTART'),
	('CM1', 'CHU', 'CHU_ARTVIS'),
	('CM1', 'CHU', 'CHU_MUSIC'),
	('CM2', 'MATHS', 'MATHS_NOMBRES'),
	('CM2', 'MATHS', 'MATHS_GEOMETRIE'),
	('CM2', 'MATHS', 'MATHS_GRANDEUR'),
	('CM2', 'MATHS', 'MATHS_ORGA'),
	('CM2', 'EPS', 'EPS_PERF'),
	('CM2', 'EPS', 'EPS_ADAPTER'),
	('CM2', 'EPS', 'EPS_EQUIPE'),
	('CM2', 'EPS', 'EPS_EXPRESSION'),
	('CM2', 'SET', 'SET_MATIERE'),
	('CM2', 'SET', 'SET_ENERGIE'),
	('CM2', 'SET', 'SET_VIVANT_UNITE'),
	('CM2', 'SET', 'SET_VIVANT_FONCTIONNEMENT'),
	('CM2', 'SET', 'SET_CORPS_HUMAIN'),
	('CM2', 'SET', 'SET_VIVANT_ENVIRONNEMENT'),
	('CM2', 'SET', 'SET_TECHNO'),
	('CM2', 'LV', 'LV_COMPREHENSION'),
	('CM2', 'LV', 'LV_EXPRESSION'),
	('CM2', 'LV', 'LV_VOCABULAIRE'),
	('CM2', 'LV', 'LV_GRAMMAIRE'),
	('CM2', 'CHU', 'CHU_HISTOIRE'),
	('CM2', 'CHU', 'CHU_GEO'),
	('CM2', 'CHU', 'CHU_ICM'),
	('CM2', 'CHU', 'CHU_HISTART'),
	('CM2', 'CHU', 'CHU_ARTVIS'),
	('CM2', 'CHU', 'CHU_MUSIC'),
	('CE2', 'MATHS', 'MATHS_NOMBRES'),
	('CE2', 'MATHS', 'MATHS_GEOMETRIE'),
	('CE2', 'MATHS', 'MATHS_GRANDEUR'),
	('CE2', 'MATHS', 'MATHS_ORGA'),
	('CE2', 'EPS', 'EPS_PERF'),
	('CE2', 'EPS', 'EPS_ADAPTER'),
	('CE2', 'EPS', 'EPS_EQUIPE'),
	('CE2', 'EPS', 'EPS_EXPRESSION'),
	('CE2', 'SET', 'SET_MATIERE'),
	('CE2', 'SET', 'SET_ENERGIE'),
	('CE2', 'SET', 'SET_VIVANT_UNITE'),
	('CE2', 'SET', 'SET_VIVANT_FONCTIONNEMENT'),
	('CE2', 'SET', 'SET_CORPS_HUMAIN'),
	('CE2', 'SET', 'SET_VIVANT_ENVIRONNEMENT'),
	('CE2', 'SET', 'SET_TECHNO'),
	('CE2', 'LV', 'LV_COMPREHENSION'),
	('CE2', 'LV', 'LV_EXPRESSION'),
	('CE2', 'LV', 'LV_VOCABULAIRE'),
	('CE2', 'LV', 'LV_GRAMMAIRE'),
	('CE2', 'CHU', 'CHU_HISTOIRE'),
	('CE2', 'CHU', 'CHU_GEO'),
	('CE2', 'CHU', 'CHU_ICM'),
	('CE2', 'CHU', 'CHU_HISTART'),
	('CE2', 'CHU', 'CHU_ARTVIS'),
	('CE2', 'CHU', 'CHU_MUSIC');


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
    sequence_id integer references sequence(id),
	ordinal integer,
    title character varying,
);
-- Deferred to the end of a transaction to allow moving elements
alter table seance add unique (sequence_id, ordinal) deferrable initially deferred;

create table etape (
  	etape_id serial primary key not null,
    ordinal integer,
    seance_id integer references seance(id),
	title character varying,
    time interval,
	objectif text,
	dispositif character varying[],
	deroulement character varying[],
	materiel_pe character varying[],
	materiel_eleve character varying[],
	consignes_criteres character varying[],
    pe_role character varying[],
)

-- Deferred to the end of a transaction to allow moving elements
alter table etape add unique (seance_id, ordinal) deferrable initially deferred;
