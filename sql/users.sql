begin;
create table "user" (
	login varchar primary key,
	password varchar,
	email varchar not null,
	firstname varchar not null,
	lastname varchar not null
);

insert into "user" (login, password, email, firstname, lastname) values  ('bleue', '$6$rounds=64927$uTk4QmsranPbk.1i$cQXcydf4GJiZLkjre3lItFNtTDoClxEWyVSWHU4vyl6v2Acbg5L7xIIwQbWIQorRKh/6HSR8uulVv4ZMbpreb/', 'anne@dupressoir.com', 'Anne', 'Dupressoir');

alter table sequence add column user_login varchar not null references "user"(login) default 'bleue';
alter table seance add column user_login varchar not null references "user"(login) default 'bleue';

alter table etape add column user_login varchar not null references "user"(login) default 'bleue';

alter table etape alter user_login drop default;
alter table seance alter user_login drop default;
alter table sequence alter user_login drop default;

alter table etape add column creation_date date default current_timestamp;
alter table seance add column creation_date date default current_timestamp;
alter table sequence add column creation_date date default current_timestamp;

alter table etape add column copy_of_etape integer references etape(etape_id);
alter table seance add column copy_of_seance integer references seance(id);
alter table sequence add column copy_of_sequence integer references sequence(id);




commit;
